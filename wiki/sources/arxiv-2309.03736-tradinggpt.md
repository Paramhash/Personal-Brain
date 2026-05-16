---
tags: [arxiv, financial-trading, multi-agent-systems, llm, research-paper]
created: 2026-05-16
reviewed: false
source_origin: "arXiv:2309.03736"
---
# arXiv:2309.03736 - TradingGPT: Multi-Agent System with Layered Memory and Distinct Characters for Enhanced Financial Trading Performance

**Title:** TradingGPT: Multi-Agent System with Layered Memory and Distinct Characters for Enhanced Financial Trading Performance
**Authors:** Li Yang, Sheng Wan, Yupeng Hou, Hui Liu, Yanling Zhi, Qi Liu, Enhong Chen
**Date:** September 2023
**URL:** https://arxiv.org/abs/2309.03736

## Abstract

TradingGPT introduces a multi-agent framework for financial trading that employs layered memory and distinct character assignments to improve trading performance. Unlike single-agent systems, TradingGPT assigns different reasoning personas and memory tiers to agents, allowing for more nuanced, context-aware decision-making across multiple time horizons.

## Key Concepts

- **Layered Memory**: Agents maintain short-term (recent events), medium-term (trend patterns), and long-term (fundamental context) memory tiers. This hierarchical memory design addresses the context window limitations of LLMs in long-horizon trading tasks.
- **Distinct Characters**: Each agent is assigned a specific "character" (risk tolerance, time horizon, analytical focus) that governs its reasoning style and output format.
- **Multi-Agent Coordination**: Multiple specialized agents collaborate to produce a consensus trading signal, similar in spirit to the [TradingAgents framework](../entities/tradingagents-framework.md) but with earlier, simpler coordination mechanisms.

## Relationship to TradingAgents

[TradingAgents](../entities/tradingagents-framework.md) cites TradingGPT in its related work as an example of reasoning-driven LLM trading agents (as opposed to news-driven or RL-driven). Key differences:
- TradingGPT focuses on layered memory as the primary differentiator; TradingAgents focuses on organizational structure and hybrid communication protocols
- TradingGPT does not implement the structured document / natural language hybrid communication that TradingAgents uses to eliminate the "telephone effect"
- TradingAgents extends the role specialization concept beyond TradingGPT's character system with a full trading firm hierarchy

## Relevance to MAOPM

The layered memory concept from TradingGPT is directly relevant to the [MAOPM initiative](../research/Current%20Research%20Initiatives.md): options portfolio management requires tracking positions across multiple time horizons (intraday delta hedges, 21–45 DTE positions, LEAPS). A layered memory architecture may be necessary for the Portfolio Manager agent to maintain context across these different temporal scales.

See also [FinMem](../concepts/llms-in-finance.md) for another implementation of layered memorization referenced in the same context.

## Related Entities and Concepts

- [TradingAgents Framework](../entities/tradingagents-framework.md) — successor framework citing this work
- [Multi-Agent LLM Financial Trading](../concepts/multi-agent-llm-financial-trading.md) — broader concept landscape
- [LLMs in Finance](../concepts/llms-in-finance.md) — categorizes TradingGPT under "reasoning-driven" LLM traders
- [Agent Role Specialization in LLM Systems](../concepts/agent-role-specialization-in-llm-systems.md) — TradingGPT's character system as precursor

---

> **Note**: This is a source stub. Full paper review pending. The abstract and key concepts above are derived from citations and summaries in [arXiv:2412.20138v7](arxiv-2412.20138v7-tradingagents.md). Verify against the original paper before citing directly.

---
