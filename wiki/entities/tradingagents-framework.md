---
tags: [llm-framework, multi-agent-system, financial-trading, ai-in-finance, research-project]
created: 2024-07-30
reviewed: false
source_origin: "[[../sources/arxiv-2412.20138v7-tradingagents.md|arXiv:2412.20138v7 - TradingAgents: Multi-Agents LLM Financial Trading]]"
---
# TradingAgents Framework

**TradingAgents** is a novel [[../concepts/multi-agent-llm-financial-trading.md|multi-agent LLM financial trading framework]] designed to replicate the collaborative dynamics of real-world trading firms. Developed by researchers from [[../entities/university-of-california-los-angeles.md|UCLA]], [[../entities/massachusetts-institute-of-technology.md|MIT]], and [[../entities/tauric-research.md|Tauric Research]], it addresses limitations in existing [[../concepts/llms-in-financial-trading.md|LLM-based financial systems]] by focusing on realistic organizational modeling and efficient communication.

## Core Architecture

The framework is structured around [[../concepts/agent-role-specialization-in-llm-systems.md|specialized LLM-powered agents]], each assigned a distinct role, goal, constraints, context, skills, and tools. This design allows for the breakdown of complex trading objectives into manageable subtasks, mirroring the structure of professional trading teams. All agents operate using the [[../entities/react-prompting-framework.md|ReAct prompting framework]], synergizing reasoning and acting.

### Agent Roles and Teams:

1.  **Analyst Team:** Responsible for gathering and analyzing diverse market data.
    *   **Fundamental Analyst Agents:** Evaluate company financials, earnings reports, and insider transactions to assess intrinsic value.
    *   **Sentiment Analyst Agents:** Process social media, news sentiment, and public information to gauge market sentiment.
    *   **News Analyst Agents:** Analyze news articles, government announcements, and macroeconomic indicators to identify market-influencing events.
    *   **Technical Analyst Agents:** Calculate and select technical indicators (e.g., MACD, RSI) to forecast price movements.

2.  **Researcher Team:** Critically evaluates information from the Analyst Team through debate.
    *   **Bullish Researchers:** Advocate for investment opportunities, highlighting positive indicators.
    *   **Bearish Researchers:** Focus on potential downsides, risks, and unfavorable market signals.
    This dialectical process aims for a balanced understanding of market conditions.

3.  **Trader Agents:** Execute trading decisions based on the comprehensive analysis from the Analyst and Researcher Teams.
    *   Evaluate recommendations, decide on timing and size of trades, place orders, and adjust portfolio allocations.

4.  **Risk Management Team:** Continuously monitors and controls the portfolio's exposure to market risks.
    *   Assesses volatility, liquidity, and counterparty risks.
    *   Implements mitigation strategies (e.g., stop-loss orders, diversification).
    *   Provides feedback to Trader Agents to ensure compliance with risk parameters.

5.  **Fund Manager:** Reviews the risk management team's discussions, determines appropriate risk adjustments, and updates the trading plan.

## Communication Protocol

TradingAgents employs a [[../concepts/structured-communication-in-multi-agent-llm-systems.md|structured communication protocol]] to enhance clarity and prevent information loss common in pure natural language systems. Agents primarily communicate through concise, well-organized reports and diagrams, extracting necessary details from a global state. Natural language dialogue is reserved for agent-to-agent conversations and debates within the Researcher and Risk Management Teams, where it promotes deeper reasoning and integration of diverse perspectives.

## Backbone LLMs

The framework strategically utilizes different [[../entities/large-language-models-llm.md|Large Language Models (LLMs)]] based on task complexity and speed requirements. Quick-thinking models (e.g., gpt-4o-mini, gpt-4o) handle low-depth tasks like summarization and data retrieval, while deep-thinking models (e.g., o1-preview) are used for reasoning-intensive tasks such as decision-making and evidence-based report writing. This approach balances efficiency with depth of reasoning and allows for seamless exchangeability of backbone models.

## Performance

Experiments on historical financial data (Jan-Mar 2024) across major tech stocks demonstrated TradingAgents' superior performance compared to [[../concepts/algorithmic-trading-strategies-baselines.md|traditional and rule-based trading strategies]]. It showed notable improvements in [[../concepts/financial-trading-performance-metrics.md|cumulative returns, Sharpe ratio, and maximum drawdown]], while also offering high explainability due to its natural language-based decision processes.

## External Links

*   **GitHub Repository:** https://github.com/TauricResearch/TradingAgents

---