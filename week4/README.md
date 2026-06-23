# Week 4: Introduction to Reinforcement Learning (RL)

## Overview
During Week 4, I explored the fundamentals of Reinforcement Learning (RL). Reinforcement Learning is a branch of Machine Learning where an agent learns to make decisions by interacting with an environment and receiving feedback in the form of rewards or penalties. The goal of the agent is to learn a strategy that maximizes cumulative rewards over time.


## What is Reinforcement Learning (RL)?
Reinforcement Learning is a learning paradigm based on **trial and error**. An agent repeatedly interacts with its environment, performs actions, and receives rewards. Over time, the agent learns which actions lead to better outcomes and improves its decision-making strategy.


## Agent-Environment Interaction
Reinforcement Learning revolves around the interaction between an **Agent** and an **Environment**.

- **Agent:** The learner or decision-maker.
- **Environment:** The world in which the agent operates.

The interaction process follows the loop:

```text
State → Action → Reward → Next State
```

At each step, the agent observes the environment, chooses an action, receives feedback, and transitions to a new state.



## States and Observations
- **State (s):** A complete description of the current condition of the environment.
- **Observation (o):** Partial information about the environment that may not contain the full state.

In many real-world problems, agents have access only to observations rather than the complete state of the environment.



## Action Spaces
The **Action Space** defines all possible actions that an agent can perform.

### Discrete Action Space
Contains a finite set of actions.

Examples:
- Move Left
- Move Right
- Jump

### Continuous Action Space
Contains real-valued actions.

Examples:
- Steering angle of a car
- Speed of a robot arm

Different action spaces often require different Reinforcement Learning algorithms.



## Policies
A **Policy** is the strategy used by an agent to decide which action to take in a given state. It maps states to actions and determines the behavior of the agent.

### Deterministic Policies
A deterministic policy always chooses the same action for a particular state.

**Example:**
```text
If traffic light is red → Stop
```

### Stochastic Policies
A stochastic policy chooses actions according to a probability distribution.

**Example:**
```text
70% → Move Left
30% → Move Right
```

Stochastic policies introduce randomness and are often useful for exploration.



## Trajectories (Episodes/Rollouts)
A **Trajectory** or **Episode** is the sequence of states and actions experienced by the agent during interaction with the environment.

**Example:**

```text
(s0, a0, s1, a1, s2, a2, ...)
```

Trajectories represent the complete history of an agent's interaction within an episode.

## Rewards and Returns

### Reward
A reward is the immediate feedback received after taking an action.

### Return
Return is the cumulative reward collected over time.

The objective of Reinforcement Learning is to learn a policy that maximizes the expected return.



## The Reinforcement Learning Optimization Problem
The central goal of Reinforcement Learning is to find an **optimal policy** that produces the highest expected cumulative reward.

In simple terms:

> Learn the best possible strategy that maximizes long-term rewards.



## Value Functions
Value functions estimate how beneficial a state or action is in terms of future rewards.

### State Value Function V(s)
Represents the expected return obtained by starting from a state and following a particular policy.

### Action-Value Function Q(s, a)
Represents the expected return obtained by taking a specific action in a state and then following a policy.

### Optimal Value Function V*(s)
Represents the maximum expected return that can be achieved from a state by following the best possible policy.

### Optimal Action-Value Function Q*(s, a)
Represents the maximum expected return achievable by taking a specific action in a state and then behaving optimally.

Value functions are fundamental components of many Reinforcement Learning algorithms because they help agents evaluate and compare decisions.



## Bellman Equations
Bellman Equations provide a recursive relationship between the value of the current state and the values of future states.

**Key Idea:**

> The value of the current state equals the immediate reward plus the expected value of future states.

Bellman Equations form the mathematical foundation of many value-based Reinforcement Learning algorithms.



## Advantage Functions
The **Advantage Function** measures how much better a specific action is compared to the average action suggested by the current policy.

It is defined as:

```text
A(s, a) = Q(s, a) - V(s)
```

A positive advantage indicates that an action is better than average, while a negative advantage indicates that it is worse than average.





