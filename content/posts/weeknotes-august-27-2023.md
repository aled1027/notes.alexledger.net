---
title: "Weeknotes: August 27 2023"
date: 2023-08-06T14:41:51-07:00
draft: false
tags: [weeknotes, llms, python, presentations]
---

## Make Presentations in HTML

I've been interested in HTML presentations of work whose main version isn't HTML, like conference talks, videos, pdfs, audio recodings, and others.

Simon Willison wrote up his approach for annotated presentations [here](https://simonwillison.net/2023/Aug/6/annotated-presentations/).

David MacKay's book Without Hot Air was written as a standard book, but is also hosted online as html  [here](https://www.withouthotair.com/).

There are many more examples beyond these two; these are just a few that came to mind.

## Using Symbex and LLM to Summarize and Make Release Notes

```sh
pipx install llm symbex


# Release notes - sometimes takes a few tries
git log -n 50 | llm --system 'release notes'

# Explain code
symbex '*' | llm --system 'explain succinctly'
symbex 'ClassName*' | llm --system 'explain succinctly'
symbex 'function_name*' | llm --system 'explain succinctly'

```

Resources

- https://simonwillison.net/2023/Aug/3/weird-world-of-llms/
- https://simonwillison.net/2023/Jun/18/symbex/
- https://simonwillison.net/2022/Jan/31/release-notes/

## What I'm Reading

- https://www.actionablebooks.com/en-ca/ (e.g., [link](https://www.actionablebooks.com/en-ca/summaries/what-to-do-when-its-your-turn-and-its-always-your-turn/))
- https://adamj.eu/tech/2021/05/11/python-type-hints-args-and-kwargs/
- [Alex Russell's blog](https://infrequently.org/)
- [Alyssa X's projects](https://www.alyssax.com/)
