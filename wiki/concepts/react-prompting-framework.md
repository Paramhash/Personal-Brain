---
tags: ["llm", "prompt-engineering", "ai-agents", "reasoning", "action", "tradingagents"]
created: 2024-05-15
reviewed: false
source_origin: "/raw/tradingagent.md"
---
# ReAct Prompting Framework

## Definition
The **ReAct (Reasoning and Acting) prompting framework** is a technique used to enhance the capabilities of [Large Language Models (LLMs)](../concepts/llms-in-finance.md) by synergizing explicit reasoning (Thought) with task-specific actions (Action). It enables LLM agents to perform complex tasks by iteratively generating thoughts, taking actions based on those thoughts, and observing the results, thereby creating a dynamic problem-solving loop.

## How it Works
The core idea of ReAct is to interleave reasoning steps with action steps:
1.  **Thought**: The LLM generates a thought, which is an internal monologue or reasoning step to plan the next action, reflect on previous observations, or break down the problem.
2.  **Action**: Based on the thought, the LLM decides on and executes an action. This action could involve using a tool (e.g., searching the web, running code, querying a database), communicating with another agent, or interacting with an environment.
3.  **Observation**: After executing the action, the LLM receives an observation, which is the result or feedback from the environment or tool.
This cycle of Thought-Action-Observation continues until the task is completed or a stopping condition is met.

## Benefits
*   **Enhanced Problem-Solving**: Allows LLMs to tackle complex, multi-step problems by breaking them down and iteratively refining their approach.
*   **Improved Factuality**: By using tools and observing real-world feedback, ReAct can reduce hallucinations and ground LLM responses in factual information.
*   **Greater Transparency**: The explicit "Thought" steps provide a clear trace of the LLM's reasoning process, enhancing explainability.
*   **Adaptability**: Agents can adapt their strategies based on observations, making them more robust in dynamic environments.

## Relevance in Financial Trading
In complex domains like financial trading, where decisions require careful reasoning, access to external data, and interaction with dynamic markets, the ReAct framework is particularly valuable.

For example, in the [TradingAgents](../entities/tradingagents.md) framework, all agents follow the ReAct prompting framework. This enables them to:
*   **Conduct Research**: An analyst agent might *think* about what data is needed, *act* by calling a financial API, and *observe* the data.
*   **Engage in Debates**: A researcher agent might *think* about a counter-argument, *act* by articulating it in dialogue, and *observe* the other agent's response.
*   **Manage Risks**: A risk management agent might *think* about potential exposures, *act* by suggesting a stop-loss, and *observe* the portfolio's updated risk profile.

The shared environment state allows agents to take context-appropriate actions, fostering a collaborative and dynamic decision-making process.

## Related Concepts
*   [LLMs in Finance](../concepts/llms-in-finance.md)
*   [Multi-Agent LLM Financial Trading](../concepts/multi-agent-llm-financial-trading.md)
*   [TradingAgents](../entities/tradingagents.md)
*   [Structured Communication Protocol](../concepts/structured-communication-protocol.md)

---