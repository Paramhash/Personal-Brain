---
tags: [machine learning, statistics, probability, sequential data, natural language processing, bioinformatics, finance]
created: 2023-10-27
reviewed: false
source_origin: "hidden markov model.md"
---
A **Hidden Markov Model (HMM)** is a statistical Markov model in which the system being modeled is assumed to be a Markov process with unobserved (hidden) states. While the actual state of the system is not directly visible, it produces **observable outputs** (or observations) that can be seen. The primary goal when working with an HMM is to infer the sequence of hidden states based solely on the sequence of visible observations.

HMMs extend the concept of a [[../concepts/markov-model.md|Markov model]] by introducing the "hidden" aspect. In a standard Markov model, all states are directly observable. In contrast, an HMM posits an underlying, unobservable Markov chain, where each hidden state generates an observable symbol according to a probability distribution.

### Core Components

An HMM is characterized by:

1.  **Hidden States (Q):** The set of unobservable states the system can be in (e.g., "Sunny," "Rainy," "Cloudy" in the roombound friend analogy).
2.  **Observable Outputs (V):** The set of symbols that can be observed (e.g., "wearing boots," "carrying umbrella," "wearing sunglasses").
3.  **Transition Probabilities (A):** The probabilities of moving from one hidden state to another (e.g., P(Rainy tomorrow | Sunny today)).
4.  **Emission Probabilities (B):** The probabilities of observing a particular output given a specific hidden state (e.g., P(carrying umbrella | Rainy)).
5.  **Initial State Probabilities (π):** The probabilities of starting in each hidden state.

### The Roombound Friend Analogy

A classic way to understand HMMs is the "roombound friend" analogy:
Imagine you are in a windowless room and want to know the weather outside (the **Hidden State**: Sunny, Rainy, Cloudy). You can't see it directly. Your friend outside tells you what they are doing or wearing (the **Observable Observation**: wearing boots, carrying an umbrella, wearing sunglasses). An HMM provides the mathematical framework to deduce the most likely weather sequence based on your friend's observations, using transition probabilities for weather changes and emission probabilities for what your friend does given the weather.

### The Three Core Problems HMMs Solve

HMMs are typically used to address three fundamental problems, each with a well-known algorithm:

1.  **Evaluation Problem:** Given an HMM and a sequence of observations, what is the probability that this model generated that sequence?
    *   **Algorithm:** [[../concepts/forward-backward-algorithm.md|Forward-Backward Algorithm]] (for computing the probability of an observation sequence).
2.  **Decoding Problem:** Given an HMM and a sequence of observations, what is the most likely sequence of hidden states that produced these observations?
    *   **Algorithm:** [[../concepts/viterbi-algorithm.md|Viterbi Algorithm]] (for finding the single best hidden state sequence).
3.  **Learning Problem:** Given a set of observation sequences, how can we estimate the HMM's parameters (transition and emission probabilities) if they are unknown?
    *   **Algorithm:** [[../concepts/baum-welch-algorithm.md|Baum-Welch Algorithm]] (an Expectation-Maximization algorithm for training HMM parameters).

### Common Real-World Use Cases

HMMs are powerful for analyzing sequential data where the underlying process is obscured by noise or indirect measurements:

*   **Speech Recognition:** Mapping noisy audio signals (observations) to spoken words or phonemes (hidden states).
*   **Bioinformatics (DNA Sequencing):** Identifying functional regions (hidden states like genes, exons) within a sequence of base pairs (observations).
*   **Quantitative Finance:** Detecting underlying market regimes (hidden states like high/low volatility) from asset price movements or trading volumes (observations).
*   **Part-of-Speech Tagging:** Assigning grammatical roles (hidden states like Noun, Verb) to words in a sentence (observations).