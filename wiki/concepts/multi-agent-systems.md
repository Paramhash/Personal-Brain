---
tags: [ai, computer-science, system-design, distributed-systems, agent-based-modeling]
created: 2024-07-30
reviewed: false
source_origin: "[[../sources/arxiv-2412.20138v7-tradingagents.md|arXiv:2412.20138v7 - TradingAgents: Multi-Agents LLM Financial Trading]]"
---
# Multi-Agent Systems

A **Multi-Agent System (MAS)** is a computerized system composed of multiple interacting intelligent agents within an environment. These agents are autonomous entities that can perceive their environment, make decisions, and take actions to achieve their goals, often in collaboration or competition with other agents.

## Key Characteristics:

*   **Autonomy:** Agents operate independently, making their own decisions without direct human or central control.
*   **Interaction:** Agents communicate and coordinate with each other to achieve individual or collective goals. This can involve cooperation, competition, or negotiation.
*   **Specialization:** Agents often have distinct roles or capabilities, allowing for the division of labor and efficient problem-solving (see [[../concepts/agent-role-specialization-in-llm-systems.md|Agent Role Specialization in LLM Systems]]).
*   **Environment:** Agents operate within a shared environment, which they can perceive and act upon.
*   **Emergent Behavior:** Complex system-level behaviors can emerge from the interactions of simpler individual agents.

## Components of an Intelligent Agent:

*   **Perception:** Ability to sense the environment.
*   **Reasoning:** Ability to process information, make decisions, and plan actions.
*   **Action:** Ability to affect the environment.
*   **Knowledge/Beliefs:** Internal representation of the environment and its own state.
*   **Goals:** Objectives the agent aims to achieve.

## Role of LLMs in Multi-Agent Systems:

With the advent of [[../entities/large-language-models-llm.md|Large Language Models (LLMs)]], agents can now leverage advanced natural language understanding, generation, and reasoning capabilities. LLMs can serve as the "brain" of individual agents, enabling them to:

*   Interpret complex instructions and roles.
*   Process diverse, unstructured information.
*   Engage in sophisticated natural language dialogue and debate.
*   Formulate detailed plans and strategies.
*   Utilize external tools and APIs effectively.

## Applications:

Multi-agent systems are applied in various domains, including:

*   **Robotics:** Coordinating multiple robots for complex tasks.
*   **Supply Chain Management:** Optimizing logistics and resource allocation.
*   **Simulations:** Modeling complex social or economic phenomena.
*   **Gaming:** Creating intelligent non-player characters.
*   **[[../concepts/multi-agent-llm-financial-trading.md|Financial Trading]]:** Simulating trading firms with specialized roles to make informed investment decisions (e.g., [[../entities/tradingagents-framework.md|TradingAgents]]).

## Communication in MAS:

Effective communication is critical in MAS. This can range from simple message passing to complex [[../concepts/structured-communication-in-multi-agent-llm-systems.md|structured communication protocols]] that ensure clarity and prevent information loss, especially when LLMs are involved.

## Related Concepts:

*   [[../entities/large-language-models-llm.md|Large Language Models (LLM)]]
*   [[../concepts/agent-role-specialization-in-llm-systems.md|Agent Role Specialization in LLM Systems]]
*   [[../concepts/structured-communication-in-multi-agent-llm-systems.md|Structured Communication in Multi-Agent LLM Systems]]
*   [[../concepts/multi-agent-llm-financial-trading.md|Multi-Agent LLM Financial Trading]]

---