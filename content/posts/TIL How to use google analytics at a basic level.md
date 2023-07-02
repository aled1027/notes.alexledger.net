---
date: 2023-04-03
tags:
  - til
  - business
title: TIL How to use google analytics at a basic level
---

# TIL How to use google analytics at a basic level

https://www.youtube.com/watch?v=mvETBDVv1eM&ab_channel=Root%26BranchDigitalMarketing

- User: a visitor who has initiated a session on your website
  - GA4 tries to de-duplicate users by: (a) user id, (b) google signals, and (c) device id.
- Event: A distinct user interaction. Loading a page, clicking a link.

There are User Groups in GA4:

1.  New Users
    - Number of people who interacted with site for the first time; `first_visit` or `first_open` event in app.
2.  Active Users
    - A user is active if they have an _engaged session_ (two or more seconds, two or more page views, criteria like that) OR when GA4 collects the `first_visit` event (i.e., they're a new user) or `engagement_time_msec` event parameters
3.  Total Users
    - Users who logged any kind of event during a time period. This is not the primary way of thinking about users in GA4.
4.  Returning Users (aka Established users)
    - Based on the Reporting Identity.

Make custom charts

1. Go to explore
2. Click Blank
3. Make the chart
