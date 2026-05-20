---
tags: [algorithms, dynamic-programming, hidden-markov-models, machine-learning, sequence-prediction]
created: 2023-10-27
reviewed: false
source_origin: "viterbi algorithm for a hidden markov model with a basic example.md"
---

# Viterbi Algorithm

The Viterbi Algorithm is a dynamic programming algorithm for finding the most likely sequence of hidden states — often referred to as the Viterbi path — that results in a sequence of observed events. It is primarily used within the context of a [[../concepts/hidden-markov-model.md|Hidden Markov Model (HMM)]] and is fundamental in fields such as speech recognition, bioinformatics, natural language processing, and telecommunications.

## Purpose

Given an HMM and a sequence of observations, the Viterbi algorithm efficiently computes the single most probable sequence of hidden states that could have generated those observations. It effectively solves the "decoding problem" in HMMs, where the goal is to infer the hidden causes from visible effects.

## Key Idea: Dynamic Programming

The algorithm leverages the principle of [[../concepts/dynamic-programming.md|dynamic programming]] to avoid redundant calculations. Instead of enumerating all possible hidden state sequences (which grows exponentially with the length of the observation sequence), it builds up the solution iteratively. At each step, it stores the probability of the most likely path to reach a given state, along with a backpointer to the previous state in that path. This allows for efficient reconstruction of the optimal path.

## Inputs

To apply the Viterbi Algorithm, you need:
1.  **Observation Sequence (O)**: The sequence of visible events (e.g., `[walk, shop, clean]`).
2.  **Hidden Markov Model (HMM) Parameters**:
    *   **Initial State Probabilities (π)**: The probability of starting in each hidden state.
    *   **Transition Probabilities (A)**: The probability of moving from one hidden state to another.
    *   **Emission Probabilities (B)**: The probability of observing a particular event from a given hidden state.

## Algorithm Steps

Let `T` be the length of the observation sequence, and `N` be the number of hidden states.

### 1. Initialization

For the first observation `O[1]` (at time `t=1`):
*   Calculate the probability of the most likely path ending in each state `s` at `t=1`. This is `V[1][s] = π[s] * B[s][O[1]]`.
*   Store a backpointer `P[1][s]` (often null or 0, as there's no preceding state).

### 2. Recursion (Forward Pass)

For `t` from `2` to `T` (for each subsequent observation `O[t]`):
For each hidden state `s_j`:
*   Calculate `V[t][s_j] = max_{s_i} (V[t-1][s_i] * A[s_i][s_j] * B[s_j][O[t]])`.
    *   This means, for each possible previous state `s_i`, find the probability of reaching `s_j` from `s_i` and emitting `O[t]`, then take the maximum over all `s_i`.
*   Store `P[t][s_j] = argmax_{s_i} (V[t-1][s_i] * A[s_i][s_j])`.
    *   This backpointer records which previous state `s_i` led to the maximum probability path ending in `s_j` at time `t`.

### 3. Termination

After processing all observations up to `T`:
*   Find the overall most likely final state: `Q_T = argmax_{s} (V[T][s])`.
*   The probability of this most likely path is `max_{s} (V[T][s])`.

### 4. Path Backtracking

Reconstruct the Viterbi path by following the backpointers from `Q_T` backwards to `Q_1`:
*   `Q_{t-1} = P[t][Q_t]` for `t` from `T` down to `2`.

The sequence `Q_1, Q_2, ..., Q_T` is the most likely sequence of hidden states.

## Basic Example: Weather Prediction

Let's consider a simplified scenario where we want to infer the weather (hidden states: `Sunny`, `Rainy`) based on daily activities (observations: `Walk`, `Shop`, `Clean`).

**HMM Parameters:**

*   **Hidden States (S)**: `Sunny`, `Rainy`
*   **Observations (O)**: `Walk`, `Shop`, `Clean`

*   **Initial Probabilities (π)**:
    *   `π[Sunny] = 0.6`
    *   `π[Rainy] = 0.4`

*   **Transition Probabilities (A)**:
    | From \ To | Sunny | Rainy |
    | :-------- | :---- | :---- |
    | Sunny     | 0.7   | 0.3   |
    | Rainy     | 0.4   | 0.6   |

*   **Emission Probabilities (B)**:
    | State \ Obs | Walk | Shop | Clean |
    | :---------- | :--- | :--- | :---- |
    | Sunny       | 0.5  | 0.3  | 0.2   |
    | Rainy       | 0.1  | 0.4  | 0.5   |

**Observation Sequence:** `O = [Walk, Shop, Clean]`

---

**Step-by-Step Calculation:**

**1. Initialization (t=1, Observation = Walk)**

*   **V[1][Sunny]**: `π[Sunny] * B[Sunny][Walk] = 0.6 * 0.5 = 0.3`
*   **V[1][Rainy]**: `π[Rainy] * B[Rainy][Walk] = 0.4 * 0.1 = 0.04`

*   `P[1][Sunny] = null`
*   `P[1][Rainy] = null`

---

**2. Recursion (t=2, Observation = Shop)**

*   **For State = Sunny:**
    *   From Sunny: `V[1][Sunny] * A[Sunny][Sunny] * B[Sunny][Shop] = 0.3 * 0.7 * 0.3 = 0.063`
    *   From Rainy: `V[1][Rainy] * A[Rainy][Sunny] * B[Sunny][Shop] = 0.04 * 0.4 * 0.3 = 0.0048`
    *   `V[2][Sunny] = max(0.063, 0.0048) = 0.063`
    *   `P[2][Sunny] = Sunny` (because 0.063 came from Sunny)

*   **For State = Rainy:**
    *   From Sunny: `V[1][Sunny] * A[Sunny][Rainy] * B[Rainy][Shop] = 0.3 * 0.3 * 0.4 = 0.036`
    *   From Rainy: `V[1][Rainy] * A[Rainy][Rainy] * B[Rainy][Shop] = 0.04 * 0.6 * 0.4 = 0.0096`
    *   `V[2][Rainy] = max(0.036, 0.0096) = 0.036`
    *   `P[2][Rainy] = Sunny` (because 0.036 came from Sunny)

---

**3. Recursion (t=3, Observation = Clean)**

*   **For State = Sunny:**
    *   From Sunny: `V[2][Sunny] * A[Sunny][Sunny] * B[Sunny][Clean] = 0.063 * 0.7 * 0.2 = 0.00882`
    *   From Rainy: `V[2][Rainy] * A[Rainy][Sunny] * B[Sunny][Clean] = 0.036 * 0.4 * 0.2 = 0.00288`
    *   `V[3][Sunny] = max(0.00882, 0.00288) = 0.00882`
    *   `P[3][Sunny] = Sunny`

*   **For State = Rainy:**
    *   From Sunny: `V[2][Sunny] * A[Sunny][Rainy] * B[Rainy][Clean] = 0.063 * 0.3 * 0.5 = 0.00945`
    *   From Rainy: `V[2][Rainy] * A[Rainy][Rainy] * B[Rainy][Clean] = 0.036 * 0.6 * 0.5 = 0.0108`
    *   `V[3][Rainy] = max(0.00945, 0.0108) = 0.0108`
    *   `P[3][Rainy] = Rainy`

---

**4. Termination**

*   `max(V[3][Sunny], V[3][Rainy]) = max(0.00882, 0.0108) = 0.0108`
*   The most likely final state `Q_3` is `Rainy`.

---

**5. Path Backtracking**

*   `Q_3 = Rainy` (from termination)
*   `Q_2 = P[3][Rainy] = Rainy`
*   `Q_1 = P[2][Rainy] = Sunny` (Note: `P[2][Rainy]` points to `Sunny` from the `t=2` step)

**Most Likely Hidden State Sequence:** `[Sunny, Rainy, Rainy]`

This means, given the observations `[Walk, Shop, Clean]`, the Viterbi algorithm suggests the most probable underlying weather sequence was `Sunny` on day 1, `Rainy` on day 2, and `Rainy` on day 3.