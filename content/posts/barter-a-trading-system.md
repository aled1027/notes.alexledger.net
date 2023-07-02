---
title: "Barter: a Trading System"
date: 2023-06-16T08:21:44-07:00
draft: true
tags: [python, fly.io, django, crypto]
---

I just shipped an alpha version of Barter, a trading system for setting up generic, automated (but not real-time), trades.

Barter works in three steps:

1. Collect data
2. Run through trading logic
3. If trade logic passes, execute the trade
4. Run through existing positions and execute close logic
5. If a position should be closed, close it.

The models supporting the five steps are:

- Instrument: A financial asset which can be purchased and sold [^1]
- InstrumentOHLC: The open, high, low, and close values at a particular datetime for an instrument.
- Position: The amount of an instrument held, including metadata
- History (likely) Some kind of history


[^1]: See https://www.investopedia.com/terms/i/instrument.asp

## Collect Data

Each day, a github action calls /api/sync_data to sync data from Coingecko ([docs](https://www.coingecko.com/en/api/documentation)). For each registered instrument that's on Coingecko, the sync services creates any new OHLC records based on the Coingecko data. 

In the future, any number of data sources can be supported, and in the current vision, they'd likely be supported by adding additional models for organizing the data.

## Run through trading logic and execute the trade

After the sync finishes, the github action calls /api/sync_new_trades which loops over the instruments and trade logic, identifying which logic passes.

The trade logic queries the database as needed to pull in whatever data it needs.

If a trade should be executed, it's also executed in this step.

## Run through existing positions and execute close logic

The github action then calls /api/sync_close_positions which loops over the positions and close logic, identifying which logic passes.

If a position should be closed, it's also closed in this step.

## An Interesting Feature in the Future: A Simulator

I'm interested in building a simulator feature where a user can put in criteria for a trade and see how it would have performed over time. This would be a great way to test out new trading strategies.

