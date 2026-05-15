---
tags: [arxiv, financial-trading, multi-agent-systems, llm, research-paper]
created: 2024-07-30
reviewed: false
source_origin: "arXiv:2412.20138v7 [q-fin.TR]"
---
# arXiv:2412.20138v7 - TradingAgents: Multi-Agents LLM Financial Trading

**Title:** TradingAgents: Multi-Agents LLM Financial Trading
**Authors:** [[../entities/yijia-xiao.md|Yijia Xiao]], [[../entities/edward-sun.md|Edward Sun]], [[../entities/di-luo.md|Di Luo]], [[../entities/wei-wang.md|Wei Wang]]
**Affiliations:** [[../entities/university-of-california-los-angeles.md|University of California, Los Angeles (UCLA)]], [[../entities/massachusetts-institute-of-technology.md|Massachusetts Institute of Technology (MIT)]], [[../entities/tauric-research.md|Tauric Research]]
**Date:** June 3, 2025 (v7)
**URL:** https://arxiv.org/abs/2412.20138

## Abstract

This paper introduces [[../entities/tradingagents-framework.md|TradingAgents]], a novel [[../concepts/multi-agent-llm-financial-trading.md|multi-agent LLM financial trading framework]] inspired by the collaborative dynamics of real-world trading firms. Unlike previous single-agent or independently data-gathering multi-agent systems, TradingAgents features [[../concepts/agent-role-specialization-in-llm-systems.md|specialized LLM-powered agents]] (e.g., fundamental, sentiment, technical analysts, traders with varied risk profiles, Bull/Bear researchers, risk management team) that synthesize insights through debate and historical data.

The framework aims to improve trading performance by simulating a dynamic, collaborative environment. Extensive experiments demonstrate its superiority over baseline models in cumulative returns, Sharpe ratio, and maximum drawdown, highlighting the potential of [[../concepts/multi-agent-llm-financial-trading.md|multi-agent LLM frameworks]] in financial trading. The TRADINGAGENTS codebase is available at https://github.com/TauricResearch/TradingAgents.

## Key Contributions:

*   **Realistic Organizational Modeling:** Simulates the decision-making processes of professional trading teams with specialized agents.
*   **Enhanced Communication Interfaces:** Combines [[../concepts/structured-communication-in-multi-agent-llm-systems.md|structured outputs]] for clarity and reasoning with natural language dialogue for debate and collaboration, addressing limitations of pure natural language communication.
*   **Comprehensive Evaluation:** Validated through experiments on historical financial data, showing significant improvements in [[../concepts/financial-trading-performance-metrics.md|cumulative return, Sharpe ratio, and maximum drawdown]] compared to [[../concepts/algorithmic-trading-strategies-baselines.md|multiple baselines]].
*   **Explainability:** [[../entities/large-language-models-llm.md|LLM]]-based agents provide natural language reasoning, enhancing the interpretability and debuggability of trading decisions.

## Related Work:

The paper discusses various applications of [[../entities/large-language-models-llm.md|LLMs]] in finance, including:
*   **LLMs as Financial Assistants:** Fine-tuned or trained-from-scratch LLMs for analytical support and information retrieval (e.g., PIXIU, FinGPT, BloombergGPT).
*   **LLMs as Traders:** Agents making direct trading decisions (e.g., news-driven, reasoning-driven like FinMem and [[../entities/tradinggpt.md|TradingGPT]], and reinforcement learning-driven agents).
*   **LLMs as Alpha Miners:** Generating alpha factors for trading strategies (e.g., QuantAgent, AlphaGPT).

## Framework Details:

[[../entities/tradingagents-framework.md|TradingAgents]] defines seven distinct agent roles:
*   **Analyst Team:** Fundamental, Sentiment, News, Technical Analysts.
*   **Researcher Team:** Bullish and Bearish Researchers engaging in debate.
*   **Trader Agents:** Execute decisions based on analysis.
*   **Risk Management Team:** Monitors and controls portfolio risk.
*   **Fund Manager:** Approves and executes trades.

All agents follow the [[../entities/react-prompting-framework.md|ReAct prompting framework]] for synergistic reasoning and acting.

## Experiments:

*   **Simulation Period:** January 1st to March 29th, 2024.
*   **Assets:** Major technology stocks (Apple, Nvidia, Microsoft, Meta, Google).
*   **Data:** Multi-modal dataset including historical stock prices, news, social media sentiment, insider transactions, financial statements, and 60 technical indicators.
*   **Baselines:** [[../concepts/algorithmic-trading-strategies-baselines.md|Buy and Hold, MACD, KDJ+RSI, ZMR, SMA]].
*   **Metrics:** [[../concepts/financial-trading-performance-metrics.md|Cumulative Return (CR), Annualized Return (AR), Sharpe Ratio (SR), Maximum Drawdown (MDD)]].

## Results:

TradingAgents consistently outperformed baselines, achieving higher cumulative and annual returns, superior Sharpe ratios (risk-adjusted returns), and maintained a relatively low maximum drawdown, demonstrating a robust balance between maximizing returns and managing risk. The framework's natural language operations also provide high explainability for trading decisions.

## Future Work:

Deployment in a live trading environment, expansion of agent roles, and incorporation of real-time data feeds.

---