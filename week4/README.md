# Week 4: Introduction to Reinforcement Learning (RL)

## Overview
During Week 4, I explored the fundamentals of Reinforcement Learning (RL).
Reinforcement Learning is a branch of Machine Learning where an agent learns to
make decisions by interacting with an environment and receiving feedback in the
form of rewards or penalties. The goal of the agent is to learn a strategy that
maximizes cumulative rewards over time.

## What is Reinforcement Learning (RL)?
Reinforcement Learning is a learning paradigm based on **trial and error**. An
agent repeatedly interacts with its environment, performs actions, and receives
rewards. Over time, the agent learns which actions lead to better outcomes and
improves its decision-making strategy.

RL has been used to teach robots to walk and recover from falls in simulation and
in the real world, to build systems that play Go and Dota at a high level, and to
learn Atari games directly from raw pixels.

## Agent-Environment Interaction
Reinforcement Learning revolves around the interaction between an **Agent** and
an **Environment**.

- **Agent:** The learner or decision-maker.
- **Environment:** The world in which the agent operates.

The interaction process follows the loop:

```text
State → Action → Reward → Next State
```

At each step, the agent observes the environment, chooses an action, receives
feedback, and transitions to a new state.

## States and Observations
- **State (s):** A complete description of the current condition of the
  environment. Nothing is hidden from the state.
- **Observation (o):** Partial information about the environment, which may omit
  parts of the state.

When the agent can see the complete state, the environment is **fully observed**.
When it can only see part of it, the environment is **partially observed**. In
practice most environments are partially observed.

Most RL notation writes `s` even in places where `o` would be more accurate,
because the agent actually conditions its action on what it observes, not on the
true underlying state.

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

Different action spaces often require different Reinforcement Learning
algorithms. Some algorithm families apply directly to only one case and need
substantial rework for the other.

## Policies
A **Policy** is the strategy used by an agent to decide which action to take in a
given state. It maps states to actions and determines the behavior of the agent.
Because the policy is effectively the agent's brain, "policy" and "agent" are
often used interchangeably.

### Deterministic Policies
A deterministic policy always chooses the same action for a particular state.
It is usually written `a = μ(s)`.

**Example:**
```text
If traffic light is red → Stop
```

### Stochastic Policies
A stochastic policy chooses actions according to a probability distribution,
written `a ~ π(·|s)`.

**Example:**
```text
70% → Move Left
30% → Move Right
```

Stochastic policies introduce randomness and are often useful for exploration.

### Parameterised Policies
In deep RL the policy is a neural network whose behaviour is controlled by a set
of parameters `θ`, the weights and biases. This is written `π_θ(·|s)` for a
stochastic policy or `μ_θ(s)` for a deterministic one. Training a policy means
adjusting `θ` with an optimisation algorithm.

For a **discrete** action space the policy is **categorical**: the network ends
in a linear layer producing one logit per action, followed by a softmax to turn
the logits into probabilities. This is the relevant case for this project, since
the arena has four moves.

For a **continuous** action space the usual choice is a **diagonal Gaussian**
policy, where a network outputs a mean action and the spread is described by a
vector of log standard deviations. Log standard deviations are used rather than
standard deviations directly, because logs can take any value while standard
deviations must stay non-negative, and unconstrained parameters are easier to
optimise.

## Trajectories (Episodes/Rollouts)
A **Trajectory** or **Episode** is the sequence of states and actions experienced
by the agent during interaction with the environment.

**Example:**

```text
(s0, a0, s1, a1, s2, a2, ...)
```

The first state is drawn from the **start-state distribution**, written
`s0 ~ ρ0(·)`. Each transition depends only on the most recent state and action,
and may be deterministic, `s_{t+1} = f(s_t, a_t)`, or stochastic,
`s_{t+1} ~ P(·|s_t, a_t)`.

Trajectories represent the complete history of an agent's interaction within an
episode.

## Rewards and Returns

### Reward
The immediate feedback received after a transition,
`r_t = R(s_t, a_t, s_{t+1})`. It can depend on where the agent was, what it did,
and where it ended up. It is often simplified to depend on just the state or the
state-action pair.

### Return
The cumulative reward over a trajectory, written `R(τ)`. There are two standard
formulations.

**Finite-horizon undiscounted return** : the plain sum over a fixed window:

```text
R(τ) = r_0 + r_1 + ... + r_T
```

**Infinite-horizon discounted return** : every reward is weighted by how far in
the future it arrives, using a **discount factor** `γ` between 0 and 1:

```text
R(τ) = r_0 + γ·r_1 + γ²·r_2 + ...
```

Why discount at all? Intuitively, a reward now is worth more than the same reward
later. Mathematically, an infinite sum of rewards need not converge to a finite
value, but with `γ < 1` and reasonable conditions it does.

`γ` is also the most practically important knob in training. With `γ` close to 1
and a positive reward for merely surviving, an agent that loops safely forever
can score higher than one that takes a risk to win, which is exactly why an
agent sometimes learns to stand still and do nothing.

## The Reinforcement Learning Optimization Problem
The central goal of Reinforcement Learning is to find an **optimal policy** that
produces the highest expected cumulative reward.

Written formally, the expected return of a policy is

```text
J(π) = E[ R(τ) ]        (expectation over trajectories produced by π)
```

and the goal is to find

```text
π* = argmax over π of J(π)
```

In simple terms:

> Learn the best possible strategy that maximizes long-term rewards.

## Value Functions
Value functions estimate how beneficial a state or action is in terms of future
rewards. By "value" we mean the expected return from starting there and then
following some policy from that point on.

### State Value Function V^π(s)
The expected return obtained by starting from a state and following policy `π`.

### Action-Value Function Q^π(s, a)
The expected return obtained by taking a specific action in a state, even one
the policy would not have chosen, and then following `π` afterwards.

### Optimal Value Function V*(s)
The maximum expected return achievable from a state by following the best
possible policy.

### Optimal Action-Value Function Q*(s, a)
The maximum expected return achievable by taking a specific action in a state and
then behaving optimally.

Two relations connect them, and both follow directly from the definitions:

```text
V^π(s) = E over a ~ π of  Q^π(s, a)
V*(s)  = max over a of    Q*(s, a)
```

The superscript matters: `V^π` is the value under a *particular* policy, `V*` is
the value under the *best possible* policy.

Value functions are fundamental components of many Reinforcement Learning
algorithms because they help agents evaluate and compare decisions.

## The Optimal Q-Function and the Optimal Action
`Q*(s, a)` gives the return from taking action `a` in state `s` and behaving
optimally afterwards. So if `Q*` is known, the best action follows immediately:

```text
a*(s) = argmax over a of Q*(s, a)
```

If several actions tie, all of them are optimal, and the optimal policy may pick
any of them. There is always an optimal policy that chooses deterministically.

This is the entire basis of value-based methods such as Q-learning, learn `Q*`,
then act greedily with respect to it.

## Bellman Equations
Bellman Equations provide a recursive relationship between the value of the
current state and the values of future states.

**Key Idea:**

> The value of your starting point is the reward you expect to get from being
> there, plus the value of wherever you land next.

For a given policy:

```text
V^π(s)    = E[ r(s,a) + γ·V^π(s') ]
Q^π(s,a)  = E[ r(s,a) + γ·E[ Q^π(s',a') ] ]
```

For the optimal value functions:

```text
V*(s)     = max over a of E[ r(s,a) + γ·V*(s') ]
Q*(s,a)   = E[ r(s,a) + γ·max over a' of Q*(s',a') ]
```

The crucial difference is the **`max` over actions**, which appears only in the
optimal equations. It expresses the fact that whenever the agent gets to choose,
acting optimally means picking whichever action leads to the highest value.

The right-hand side, reward plus discounted next value, is called the
**Bellman backup**.

Bellman Equations form the mathematical foundation of many value-based
Reinforcement Learning algorithms.

## Advantage Functions
The **Advantage Function** measures how much better a specific action is compared
to the average action suggested by the current policy, assuming the policy is
followed from then on.

It is defined as:

```text
A(s, a) = Q(s, a) - V(s)
```

A positive advantage indicates that an action is better than average, while a
negative advantage indicates that it is worse than average.

The advantage function is central to policy gradient methods, including PPO,
which is the algorithm used in the later weeks of this project.

## Formalism: Markov Decision Processes
The standard mathematical model for this setting is a **Markov Decision Process**
(MDP), a 5-tuple `⟨S, A, R, P, ρ0⟩`:

| Symbol | Meaning |
|---|---|
| `S` | the set of all valid states |
| `A` | the set of all valid actions |
| `R` | the reward function, `r_t = R(s_t, a_t, s_{t+1})` |
| `P` | the transition function, the probability of reaching `s'` from `s` via `a` |
| `ρ0` | the starting state distribution |

The name refers to the **Markov property**: transitions depend only on the most
recent state and action, with no dependence on earlier history.

## Mapping This to the RL Arena
The Paper.io game built in Week 3 is already an MDP:

| MDP element | RL Arena |
|---|---|
| `S` | the grid (`0`, `±1`, `±2`), the agent's head position and direction, steps remaining |
| `A` | four discrete moves - up, right, down, left |
| `R` | territory gained, trail length, killing the opponent, dying |
| `P` | the movement and collision rules in `game.py` |
| `ρ0` | the starting territories and spawn positions |

The distinction between **state** and **observation** matters here in practice.
The full grid is the state, but an agent is normally given a reduced view of it.
If something that can kill the agent, its own trail, for instance, is left out
of that view, the environment becomes partially observed and the agent cannot
learn to avoid it, no matter how the reward is tuned. Likewise, if an episode has
a time limit, the remaining time belongs in the observation, or the agent is
racing a clock it cannot see.

The discount factor also has a direct consequence for this game. A reward for
simply staying alive, combined with a `γ` close to 1, makes an endless safe loop
more valuable than a risky capture , so surviving should carry a small cost, not
a bonus.
