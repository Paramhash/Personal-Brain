---
domain: cl-market-making
tags: [curriculum, reading-list]
aliases: [CL reading list]
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
---

# Seed sources for the CL / market-making / timing curriculum

**Before downloading, check each title, year and edition**: this list was compiled from memory, not from a search.
Drop sources into `raw/` in batches of about five, run `python ingest.py --once`, and read the ingestion log
(created / merged / rejected) before the next batch. Tick a source off when it has been ingested.

Back to [[00-cl-mm-timing-moc|the map of content]].

## Already available from the bot (exported by `bridges/dlmm_bridge.py`)
- [x] Milionis, Moallemi, Roughgarden, Zhang — *Automated Market Making and Loss-Versus-Rebalancing* (2022): `raw/dlmm-amm-and-loss-versus-rebalancing.pdf` · M4
- [x] Bot research notes 00–02 (dual-inventory growth, warehouse-manager inventory strategy, Nash LP strategies): `raw/dlmm-0*.md` · M7, M11
- [x] Bot findings (EV gate calibration and vs simulator, pool σ forecast, fee counters, F-021/022/024/026): `raw/dlmm-*.md` · M4–M6, M10

## AMMs and concentrated liquidity (M1–M3)
- [ ] Adams, Zinsmeister, Salem, Keefer, Robinson — *Uniswap v3 Core* whitepaper (2021)
- [ ] Trader Joe — *Liquidity Book* whitepaper (the bin design DLMM follows)
- [ ] Meteora — DLMM documentation (bins, bin step, dynamic fees, strategies Spot / Curve / BidAsk)
- [ ] Orca — Whirlpools documentation (ticks, tick spacing)
- [ ] Angeris, Chitra — *Improved Price Oracles: Constant Function Market Makers* (2020)

## LVR, impermanent loss and LP returns (M4–M5)
- [ ] Milionis, Moallemi, Roughgarden — *Automated Market Making and Arbitrage Profits in the Presence of Fees* (2023)
- [ ] Cartea, Drissi, Monga — *Decentralised Finance and Automated Market Making: Predictable Loss and Optimal Liquidity Provision*
- [ ] Loesch, Hindman, Richardson, Welch — *Impermanent Loss in Uniswap v3* (2021)
- [ ] Heimbach, Schertenleib, Wattenhofer — *Risks and Returns of Uniswap V3 Liquidity Providers* (2022)
- [ ] Hasbrouck, Rivera, Saleh — *The Need for Fees at a DEX* (2022)

## Volatility (M6)
- [ ] Corsi — *A Simple Approximate Long-Memory Model of Realized Volatility* (HAR-RV, 2009)
- [ ] Patton — *Volatility Forecast Comparison Using Imperfect Volatility Proxies* (2011)
- [ ] Andersen, Bollerslev, Diebold, Labys — *Modeling and Forecasting Realized Volatility* (2003)

## Market making and inventory (M7)
- [ ] Ho, Stoll — *Optimal Dealer Pricing under Transactions and Return Uncertainty* (1981)
- [ ] Glosten, Milgrom — *Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders* (1985)
- [ ] Kyle — *Continuous Auctions and Insider Trading* (1985)
- [ ] Avellaneda, Stoikov — *High-Frequency Trading in a Limit Order Book* (2008)
- [ ] Guéant, Lehalle, Fernandez-Tapia — *Dealing with the Inventory Risk* (2013)
- [ ] Guéant — *The Financial Mathematics of Market Liquidity* (book)
- [ ] Cartea, Jaimungal, Penalva — *Algorithmic and High-Frequency Trading* (book)

## Hedging, perpetuals and funding (M8–M9)
- [ ] Fukasawa, Maire, Wunsch — *Weighted Variance Swaps Hedge against Impermanent Loss*
- [ ] Lambert — articles on Uniswap v3 LP positions as options
- [ ] He, Manela, Ross, von Wachter — *Fundamentals of Perpetual Futures*
- [ ] Ackerer, Hugonnier, Jermann — *Perpetual Futures Pricing*

## Timing and dealer gamma (M10)
- [ ] SqueezeMetrics — *Gamma Exposure (GEX)* white paper (the vault already has [[gamma-exposure-gex]])
- [ ] Barbon, Buraschi — *Gamma Fragility*
- [ ] Moskowitz, Ooi, Pedersen — *Time Series Momentum* (2012), for what timing evidence does and does not show

## Strategic LPs (M11)
- [ ] Capponi, Jia — *The Adoption of Blockchain-based Decentralized Exchanges*
- [ ] Research on just-in-time (JIT) liquidity on Uniswap v3 (search for a current survey)
