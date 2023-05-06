---
date: 2023-05-06
tags:
    - finance
    - python
    - software
title: Manage Your Money
---

# Manage Your Money

Manage Your Money is my 10th? 15th? attempt at writing a system for managing my personal finances.

Each time, I fall back to the convenience of a SaaS tool; but inevitably, a few days, weeks, or months later, I get frustrated with the SaaS tool for one reason or another: 

- Unreliable syncing: Mint and Personal Capital frequently get disconnected from Venmo.
- Unreliable transaction processing: Personal Capital classified my rent as income, and to make it worse, I had to email their support to change it - there was no way for me to revise in their app.
- Dubious ethics: Intuit has a record of shady practices
- Poor transaction process tooling: Personal Capital didn't have features for applying human-informed rules about categorizing transactions. 

To be fair, I didn't try YNAB or other paid providers.

When writing my own financial tools, I'd often encounter some challenges that I wasn't quite sure how to address from either a UX or technical perspective. These include (below I say how I resolve or avoid these):

- Auto-downloading financial data
- Processing duplicate transactions: If two identical records come in, can I deduplicate them? Often, I'll buy the same thing for the same price from the same merchant in a single day.
- Categorize the purchase for analysis
- Store the data in an easily consumable way
- Handling transfers between accounts is tricky

## My Current Approach

I now have an approach - which I may not agree with in a few months, but for now I'm happy with - for each of those pain points.

- I gave up automatically downloading financial data
- I gave up on trying to prevent processing duplicate transactions. Now I'm careful about downloading data and slicing it up per month in a data download & prep step
- I use my credit card's purchase categorizations and have simple rules in place for correcting where I disagree
- I'm uploading the results of the processing into a Google sheet, and I then use Google sheet formulas for processing.
- I basically avoid transfers, just don't care about them. They're so tricky, so I give them an annotation ignore and don't look very closely at them. My primary goal is to understand where and how much I spend, not bookkeeping.

Another day I'll expound upon my many false starts.

The approach now is the following:

1. At the beginning of each month, download a CSV of the previous month's data
2. Put the data into the right location of a directory
3. Run a Python script that outputs a CSV with conformed financial data
4. Upload the CSV into an existing Google sheet table (append rows)
5. Manually inspect, annotate, and correct any data issues

I had been avoiding a process like this because I had thought step 1 would be too annoying. So for a while, I would aggregate the data into Mint and export from there, but I found downloading the data from my current financial institutions is pretty easy; it was more challenging with my previous financial institutions.

### Design of the Python Script

The Python script has a moderately interesting design.

The data is placed into directories that're organized by financial institutions. Each directory is loaded using a particular loader function that knows how to handle the idiosyncrasies of the format and outputs a pandas dataframe with a specific set of columns.

The dataframes are combined into one large dataframe with the following columns:

- Date: The date the transaction occurred
- Description (basically merchant): Description of the transaction from the financial institution.
- Category: The budget category of the transaction (e.g., income, restaurant)
- Amount: The amount of the transaction. if positive, then I was paid; if negative, I paid someone. Transfers are more or less ignored.
- Source: The source account of the transaction. I adapted the system from Beancount such that the names are like `cc:cap1` for the cap1 credit card.
- Type: The type of the transaction. It must be one of `income`, `expense`, `expense:reimbursable`, `expense:aberration`, `ignore`, or `unknown`.

A series of rules are applied to rows in the dataframe. The rows are easy to make because they use a Python decorator like so:

```python
rules_registry: OrderedDict[str, Any] = OrderedDict()


def register_rule(name: str):
    def decorator(func):
        rules_registry[name] = func
        return func

    return decorator


def apply_rules(df):
    for name, rule in rules_registry.items():
        df = rule(df)
    return df


@register_rule("identify_income")
def rule_identify_income(df):
    # Set to income
    substrs = ["TRINET", "GUSTO"]
    for substr in substrs:
        df.loc[df["description"].str.contains(substr), "type"] = "income"
    return df

@register_rule("identify_rent")
def rule_identify_rent(df):
    substrs = ["BRISTOL EQUITIES", "APTS LEDGER"]
    for substr in substrs:
        # Mask if it matches the substring and has type unknown
        mask = (df["description"].str.contains(substr)) & (df["type"] == "unknown")
        df.loc[mask, "type"] = "expense"
    return df
```

After the rules are applied, the dataframe is output to a CSV. I'm manually importing the CSV into google sheets, but that's scriptable in the future if desired.

### Analyzing in Google Sheets

I manually peruse and correct the transactions table in google sheets.

I set up a roll-up table where I use a series of SUMIFs to aggregate the data for each month. For example, I use the following formula to get all the expenses for a month:

```
=SUMIFS(Transactions!$D$1:D, Transactions!$F$1:F, "expense", Transactions!A:A, ">="&A64, Transactions!A:A, "<"&EOMONTH(A64, 0)+1)
```

This formula isn't that useful out of context, but it: (a) sums up the amount column, which is Column D, (b) filters to only transactions with the type expense in column F, (d) filters to only transactions that came after the date in A64 and (d) filters to transactions that came before one month. 

