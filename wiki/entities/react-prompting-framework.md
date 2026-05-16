---
tags:
  - llm
  - prompting-techniques
  - agent-design
  - reasoning
  - action
created: 2024-07-30
reviewed: true
source_origin: "[[../sources/arxiv-2412.20138v7-tradingagents.md|arXiv:2412.20138v7 - TradingAgents: Multi-Agents LLM Financial Trading]]"
---
# ReAct Prompting Framework

The **ReAct (Reasoning and Acting)** prompting framework is a technique used to enhance the capabilities of [[../entities/large-language-models-llm.md|Large Language Models (LLMs)]] by synergizing explicit reasoning with task-specific actions. It allows LLMs to generate reasoning traces and take actions in an interleaved manner, leading to more robust and effective problem-solving.

## Core Principle

ReAct combines two key components:

1.  **Reasoning (Thought):** The LLM generates internal thoughts or reasoning steps to plan, analyze, and reflect on the problem. This helps in breaking down complex tasks, identifying necessary information, and formulating strategies.
2.  **Acting (Action):** Based on its reasoning, the LLM decides to take specific actions, often by calling external tools or APIs. These actions interact with the environment, retrieve information, or perform operations.

The output of an action (e.g., tool observation) then feeds back into the LLM's context, allowing it to refine its reasoning and decide on subsequent actions. This iterative loop enables dynamic and adaptive problem-solving.

## Benefits

*   **Improved Problem-Solving:** By explicitly reasoning and acting, LLMs can tackle more complex, multi-step tasks.
*   **Enhanced Explainability:** The generated reasoning traces provide transparency into the LLM's decision-making process, making it easier to understand and debug.
*   **Tool Integration:** Facilitates the seamless integration of external tools, extending the LLM's capabilities beyond its inherent knowledge.
*   **Reduced Hallucinations:** The ability to query external tools for factual information can help mitigate the risk of LLMs generating incorrect or fabricated responses.
*   **Dynamic Adaptation:** The interleaved nature allows the LLM to adapt its plan based on real-time observations from its actions.

## Application in TradingAgents

In the [[../entities/tradingagents-framework.md|TradingAgents framework]], all specialized agents (e.g., analysts, researchers, traders, risk managers) follow the ReAct prompting framework. This design enables them to:

*   **Conduct Research:** Reason about what information is needed and then use tools (e.g., `get_YFin_data`, `get_finnhub_news`) to retrieve it.
*   **Execute Trades:** Reason about optimal trading actions and then execute buy/sell orders.
*   **Engage in Debates:** Reason about arguments and counter-arguments, then formulate responses.
*   **Manage Risks:** Reason about portfolio exposure and implement mitigation strategies.

The shared environment state is monitored by agents, allowing them to take context-appropriate actions and contribute to a collaborative, dynamic decision-making process.

## Related Concepts:

*   [[../entities/large-language-models-llm.md|Large Language Models (LLM)]]
*   [[../concepts/multi-agent-systems.md|Multi-Agent Systems]]
*   [[../concepts/agent-role-specialization-in-llm-systems.md|Agent Role Specialization in LLM Systems]]

---