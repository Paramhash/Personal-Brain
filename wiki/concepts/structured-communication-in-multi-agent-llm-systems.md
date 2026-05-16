---
tags: [multi-agent-systems, llm, communication-protocol, system-design, information-flow]
created: 2024-07-30
reviewed: false
source_origin: "[[../sources/arxiv-2412.20138v7-tradingagents.md|arXiv:2412.20138v7 - TradingAgents: Multi-Agents LLM Financial Trading]]"
---
# Structured Communication in Multi-Agent LLM Systems

**Structured communication** in [[../concepts/multi-agent-systems.md|multi-agent systems]] powered by [[../entities/large-language-models-llm.md|Large Language Models (LLMs)]] refers to the use of predefined formats, protocols, and shared states for agents to exchange information, rather than relying solely on unstructured natural language dialogue. This approach is crucial for solving complex, long-term tasks where maintaining context, preventing information loss, and ensuring precision are paramount.

## Limitations of Pure Natural Language Communication:

*   **"Telephone Effect":** Information can be lost or distorted as conversations lengthen and pass through multiple agents.
*   **Context Length Limitations:** LLMs have finite context windows, making it challenging to maintain long message histories without losing critical earlier details.
*   **Information Overload:** Unstructured pools of information can obscure critical data, making it difficult for agents to filter relevant details.
*   **Lack of Relational Integrity:** Without clear instructions or formats, logical communication and information exchange can become haphazard.

## Benefits of Structured Communication:

*   **Clarity and Precision:** Information is encapsulated in concise, well-organized reports or data structures, preserving essential content.
*   **Reduced Message Corruption:** Predefined states and formats minimize the risk of details being forgotten or distorted.
*   **Efficient Information Exchange:** Agents can query necessary details directly from a global or shared state, reducing the need for lengthy, redundant conversations.
*   **Enhanced Reasoning:** By providing clear, structured inputs, agents can focus their reasoning on the relevant data.
*   **Control and Traceability:** The flow of information is more controlled and traceable, aiding in debugging and understanding the system's decision-making process.

## Implementation Approaches (as seen in TradingAgents):

The [[../entities/tradingagents-framework.md|TradingAgents framework]] exemplifies a hybrid approach:

1.  **Structured Documents and Reports:**
    *   **Analyst Team:** Compiles research and findings into concise analysis reports specific to their expertise (e.g., fundamental, sentiment, news, technical reports).
    *   **Traders:** Produce clear decision signals accompanied by detailed reports explaining their rationale and supporting evidence.
    *   **Shared Global State:** These structured reports are recorded in a global agent state, allowing other agents to access and query necessary details directly.

2.  **Natural Language Dialogue (for specific interactions):**
    *   **Researcher Team:** Engages in multi-round natural language debates (e.g., bullish vs. bearish perspectives) to promote deeper reasoning and integrate diverse viewpoints. The outcome of these debates is then recorded as a structured entry.
    *   **Risk Management Team:** Deliberates from various perspectives (risk-seeking, neutral, risk-conservative) through natural language discussion to adjust trading plans.

This hybrid model ensures both precision and flexibility, leveraging the strengths of both structured data and natural language interaction.

## Related Concepts:

*   [[../concepts/multi-agent-systems.md|Multi-Agent Systems]]
*   [[../concepts/agent-role-specialization-in-llm-systems.md|Agent Role Specialization in LLM Systems]]
*   [[../concepts/multi-agent-llm-financial-trading.md|Multi-Agent LLM Financial Trading]]

---