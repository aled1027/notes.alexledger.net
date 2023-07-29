---
title: "Barter: A Trading System"
date: 2023-07-29
draft: false
tags: [python, django, crypto]
---

I published a pre-alpha version of Barter, a trading system for setting up generic, automated (but not real-time), trades Right now, the system is built for dydx. The code is a work in progress - presently, only opening positions is supported and closing them is not (not a great way to profit :)).

Link to repo: https://github.com/aled1027/barter

Barter works in three steps:

1. Collect data
2. Run through trade logic. If a position should be opened, open it.
3. Run through existing positions. If a position should be closed, close it. (Not yet implemented)
4. If a position should be closed, close it.

## Collect Data

Each day, data is synced from dydx for each instrument that's registered in the database. In the future, any number of data sources can be supported, and in the current vision, they'd likely be supported by adding additional models for organizing the data.

## Run through trading logic and execute the trade

After the sync finishes, a cron job executes a process that loops over the instruments and trade logic, identifying which logic passes. The trade logic queries the database as needed to pull in whatever data it needs. If a trade should be executed, it's also executed in this step.

## An Interesting Feature in the Future: A Simulator

I'm interested in building a simulator feature where a user can put in criteria for a trade and see how it would have performed over time. This would be a great way to test out new trading strategies.
