---
tags: [ai, machine-learning, natural-language-processing, deep-learning, foundation-models]
created: 2024-07-30
reviewed: false
source_origin: "[[../sources/arxiv-2412.20138v7-tradingagents.md|arXiv:2412.20138v7 - TradingAgents: Multi-Agents LLM Financial Trading]]"
---
# Large Language Models (LLM)

**Large Language Models (LLMs)** are a class of artificial intelligence models, typically based on transformer architectures, that are trained on vast amounts of text data. They are capable of understanding, generating, and processing human language with remarkable fluency and coherence.

## Key Characteristics:

*   **Scale:** Characterized by billions or even trillions of parameters, enabling them to capture complex linguistic patterns.
*   **Pre-training:** Undergo extensive pre-training on diverse text corpora, learning general language understanding and generation capabilities.
*   **Fine-tuning:** Can be fine-tuned on smaller, domain-specific datasets to adapt to particular tasks or industries (e.g., finance, medicine).
*   **Emergent Abilities:** Exhibit emergent abilities such as reasoning, common sense, and problem-solving, which are not explicitly programmed but arise from their scale and training.

## Applications:

LLMs have a wide range of applications across various fields, including:

*   **Content Generation:** Writing articles, summaries, creative text.
*   **Translation:** Translating between languages.
*   **Question Answering:** Providing informative answers to queries.
*   **Code Generation:** Assisting with programming tasks.
*   **[[../concepts/llms-in-financial-trading.md|Financial Analysis and Trading]]:** Processing financial reports, news sentiment, and assisting in trading decisions (e.g., [[../entities/tradingagents-framework.md|TradingAgents]]).

## Role in Multi-Agent Systems:

In [[../concepts/multi-agent-systems.md|multi-agent systems]], LLMs serve as the "brains" of individual agents, enabling them to:

*   **Understand Instructions:** Interpret their assigned roles and goals.
*   **Process Information:** Analyze diverse inputs (textual, numerical, multimodal).
*   **Reason and Plan:** Formulate strategies and make decisions.
*   **Communicate:** Interact with other agents and external systems, often following [[../concepts/structured-communication-in-multi-agent-llm-systems.md|structured communication protocols]].
*   **Utilize Tools:** Integrate and use external tools (e.g., APIs, calculators) to augment their capabilities.

## Examples of LLMs:

*   GPT-3.5, GPT-4, gpt-4o, gpt-4o-mini (OpenAI)
*   o1-preview (OpenAI)
*   LLaMA (Meta)
*   BloombergGPT
*   Qwen
*   Baichuan
*   FinGPT
*   PIXIU (FinMA)
*   XuanYuan 2.0
*   Fin-T5

## Related Concepts:

*   [[../concepts/multi-agent-systems.md|Multi-Agent Systems]]
*   [[../concepts/llms-in-financial-trading.md|LLMs in Financial Trading]]
*   [[../entities/react-prompting-framework.md|ReAct Prompting Framework]]

---