---
title: "Doing a Group By On Datadog Logs"
date: 2023-08-31T08:41:25-07:00
draft: false
tags: [datadog, python, datasette, logs, monitoring]
---

I had some queries that were timing out in a web app, which were identified by a log pattern where a log `request_started` was logged but a log with `request_finished` wasn't. I wanted to finf queries that matched that pattern and as far as I could tell, datadog didn't support an aggregate query like this. So I exported the data to a CSV and queried it directly. 

1. Go to datadog logs and add the query and time range. My query was `service:odyn-prod @event:request_*`.
2. Dump the logs: click Download as CSV. I download about 60k rows and it took <90 seconds.
3. I wanted to use datasette, so I converted the csv into a sqlite database: `sqlite-utils insert data.db data data.csv --csv`
4. I opened the database with datasette: `datasette data.db`
5. I ran this query:

```sql
with og as (
  select
    rowid,
    Date,
    Host,
    Service,
    [@log.level],
    [@code],
    [@event],
    Message,
    json_extract(Message, '$.request_id') as request_id,
    json_extract(Message, '$.request') as request
  from
    data
)
select
  request_id,
  count(*) as c,
  group_concat([@event], ' | ') as m,
  group_concat(request, ' | ') as request
from
  og
group by
  request_id
order by
  c
```

If you're running datasette locally with the steps above, you can visit this [link](http://127.0.0.1:8001/data?sql=with+og+as+%28%0D%0A++select%0D%0A++++rowid%2C%0D%0A++++Date%2C%0D%0A++++Host%2C%0D%0A++++Service%2C%0D%0A++++%5B%40log.level%5D%2C%0D%0A++++%5B%40code%5D%2C%0D%0A++++%5B%40event%5D%2C%0D%0A++++Message%2C%0D%0A++++json_extract%28Message%2C+%27%24.request_id%27%29+as+request_id%2C%0D%0A++++json_extract%28Message%2C+%27%24.request%27%29+as+request%0D%0A++from%0D%0A++++data%0D%0A%29%0D%0Aselect%0D%0A++request_id%2C%0D%0A++count%28*%29+as+c%2C%0D%0A++group_concat%28%5B%40event%5D%2C+%27+%7C+%27%29+as+m%2C%0D%0A++group_concat%28request%2C+%27+%7C+%27%29+as+request%0D%0Afrom%0D%0A++og%0D%0A%0D%0Agroup+by%0D%0A++request_id%0D%0Aorder+by%0D%0A++c).


![Screenshot of query and query results](/2023-08-31-logs.png#center)