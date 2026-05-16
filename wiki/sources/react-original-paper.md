---
tags: [arxiv, llm, reasoning, prompting, research-paper, foundational]
created: 2026-05-16
reviewed: false
source_origin: "arXiv:2210.03629"
---
# arXiv:2210.03629 - ReAct: Synergizing Reasoning and Acting in Language Models

**Title:** ReAct: Synergizing Reasoning and Acting in Language Models
**Authors:** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
**Affiliations:** Princeton University, Google Research
**Date:** October 2022 (v1); ICLR 2023
**URL:** https://arxiv.org/abs/2210.03629

## Abstract

ReAct proposes a general paradigm that synergizes **Rea**soning and **Act**ing in language models. Rather than using LLMs for reasoning-only (chain-of-thought) or acting-only (action prediction), ReAct interleaves verbal reasoning traces with discrete actions, forming a loop that allows models to update plans based on observations from tool use and environment feedback.

## Core Mechanism

The ReAct loop follows a repeating cycle:

```
Thought → Action → Observation → Thought → Action → Observation → ...
```

- **Thought**: Internal reasoning — plan, decompose, reflect on prior observations
- **Action**: Tool call, API call, information retrieval, or environment interaction
- **Observation**: Feedback from the environment (tool output, search result, error)

The loop continues until the task is complete or a terminal condition is reached.

## Key Contributions

- **Reduces hallucination**: Grounding reasoning in real observations (rather than pure chain-of-thought) reduces confabulation in factual tasks
- **Improves interpretability**: The interleaved reasoning traces make agent decision-making transparent and debuggable
- **Generalizes across tasks**: Demonstrated on question answering (HotpotQA), fact verification (Fever), and interactive decision-making (ALFWorld, WebShop)
- **Enables dynamic replanning**: Agents can observe failed actions and revise strategy mid-task, unlike fixed chain-of-thought

## Relationship to TradingAgents / MAOPM

The [ReAct Prompting Framework](../concepts/react-prompting-framework.md) is the foundational reasoning pattern used by all agents in the [TradingAgents framework](../entities/tradingagents-framework.md) and is carried forward directly into [MAOPM](../research/Current%20Research%20Initiatives.md):

- **Analysts** use ReAct to retrieve market data, compute metrics, and iteratively refine reports
- **Researchers** use ReAct to search for supporting evidence, challenge assumptions, and update debate positions
- **Portfolio Manager** uses ReAct to evaluate strategy proposals against Greek targets and request additional analysis if needed
- **Risk Team** uses ReAct to assess position proposals and iterate with the Portfolio Manager on sizing

The key benefit in options portfolio management is that ReAct's observation loop allows agents to catch data errors (e.g., stale Greeks), request updated data, and revise decisions before committing to a trade — critical for a domain where numerical precision matters.

## Why This Paper Matters to the Vault

Before this paper, the [react-prompting-framework concept](../concepts/react-prompting-framework.md) was documented without a source reference. This paper is the primary citation for that concept and should be linked anywhere ReAct is used as a design justification.

## Citation

```
@inproceedings{yao2023react,
  title={ReAct: Synergizing Reasoning and Acting in Language Models},
  author={Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and Du, Nan and Shafran, Izhak and Narasimhan, Karthik and Cao, Yuan},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2023},
  url={https://arxiv.org/abs/2210.03629}
}
```

## Related Concepts and Entities

- [ReAct Prompting Framework](../concepts/react-prompting-framework.md) — vault concept documenting this paradigm
- [TradingAgents Framework](../entities/tradingagents-framework.md) — applies ReAct to all agent roles
- [Multi-Agent Systems](../concepts/multi-agent-systems.md) — ReAct as the per-agent reasoning backbone
- [Agent Role Specialization in LLM Systems](../concepts/agent-role-specialization-in-llm-systems.md) — each role uses ReAct with domain-specific tools

---
