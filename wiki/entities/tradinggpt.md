---
tags: ["entity", "llm", "financial-trading", "multi-agent-systems"]
created: 2026-05-16
reviewed: false
source_origin: "arXiv:2309.03736"
---
# TradingGPT

TradingGPT is a multi-agent LLM framework for financial trading that uses **layered memory** and **distinct character assignments** to improve trading performance across multiple time horizons.

## Key Design Choices

- **Layered Memory**: Short-term (recent events), medium-term (trends), and long-term (fundamentals) memory tiers address LLM context window limitations in trading tasks
- **Distinct Characters**: Each agent is assigned a persona (risk tolerance, time horizon, analytical focus) that governs its reasoning style — a precursor to the full role specialization seen in [TradingAgents](tradingagents-framework.md)
- **Multi-Agent Coordination**: Agents produce a consensus signal, though coordination is simpler than TradingAgents' hybrid structured/dialogue communication approach

## Source

Full details: [arXiv:2309.03736](../sources/arxiv-2309.03736-tradinggpt.md)

## Relationship to Other Frameworks

Referenced in [TradingAgents (arXiv:2412.20138v7)](../sources/arxiv-2412.20138v7-tradingagents.md) as a "reasoning-driven" LLM trading agent, in contrast to news-driven and reinforcement learning-driven approaches.

The layered memory concept is relevant to the [MAOPM initiative](../research/Current%20Research%20Initiatives.md), which must manage options positions across multiple time horizons (intraday hedges, 21–45 DTE positions, LEAPS).

## Related Concepts

- [Multi-Agent LLM Financial Trading](../concepts/multi-agent-llm-financial-trading.md)
- [LLMs in Finance](../concepts/llms-in-finance.md)
- [Agent Role Specialization in LLM Systems](../concepts/agent-role-specialization-in-llm-systems.md)

---
