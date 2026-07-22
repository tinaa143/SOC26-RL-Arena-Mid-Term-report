# Week 6 — RL Arena as a Gym Environment

The Week 3 Paper.io game turned into a Gymnasium environment so a PPO agent can
play it. One agent against a static enemy on a 15×15 grid.

## How to Run

```
pip install -r requirements.txt
python3 train.py     # trains and saves paper_io_agent.zip
python3 play.py      # watch the trained agent
```

## Grid Encoding

Same as Week 3:

```
 0   empty
+1   agent territory     -1   agent trail
+2   enemy territory     -2   enemy trail
```

## Rules

- The enemy never moves. Its territory **blocks** the agent.
- Touching the enemy **trail** kills the enemy and frees its territory, the
  agent wins and the episode ends.
- Touching the agent's **own** trail kills the agent.
- The grid edge and enemy territory block the agent rather than killing it.
- If time runs out, the agent wins by having more territory than the enemy.

Both sides start with a 3×3 territory. The enemy position and the direction of
its 5-cell trail are randomised every episode, so the agent has to find the
enemy rather than memorise one route.

## Spaces

| | |
|---|---|
| Action space | `Discrete(4)` — up, right, down, left |
| Observation space | `Box(0, 1, (15, 15, 3), float32)` |
| Episode limit | 200 steps |

## Observation

| Channel | Contents |
|---|---|
| 0 | your territory `1.0`, **your trail `0.5`** |
| 1 | enemy territory `1.0` |
| 2 | enemy trail `1.0`, your head `0.5` |

**Deviation from the assignment, and why.** The channel layout in the brief puts
your territory in channel 0 and leaves your own trail out of the observation
entirely. But touching your own trail is fatal, so an agent that cannot see it
is being asked to avoid something invisible. That makes the environment
partially observed in a way no amount of reward tuning can fix, the agent has
no signal to learn from. Adding the trail at `0.5` in channel 0 keeps the
observation at three channels while making every fatal cell visible.

### Grid vs Observation

The **grid** is the game logic — signed integers. The **observation** is what
the agent sees, three channels of floats in `[0, 1]`. `_get_obs()` converts one
to the other.

## Rewards

| Event | Value |
|---|---|
| Every step | `-0.01` |
| Change in (my cells − enemy cells) | `× 0.2` |
| Killing the enemy | `+10.0`, episode ends |
| Dying on your own trail | `-10.0`, episode ends |
| Time out with more territory | `+5.0` |
| Time out with less territory | `-5.0` |

The territory reward is based on the **change in the gap**, not on the agent's
own count. Capturing ten tiles is worth nothing if the enemy still has twenty,
so rewarding the difference expresses the actual win condition directly. It also
handles the kill cleanly: when the enemy dies its territory drops to zero and the
gap widens on its own.

The per-step cost is a small **penalty** rather than a survival bonus. With a
discount factor close to 1, any positive reward for merely staying alive makes an
endless safe loop more valuable than a risky capture, and the agent learns to
stand still.

## Status and Next Steps

The environment is complete and passes `stable_baselines3`'s `check_env`.
Verified behaviour: the enemy trail is always 5 cells, both sides always start
with 9 territory cells, the enemy spawn varies every episode, own-trail death
fires correctly, capture works, and episodes truncate at 200 steps.

The reward values above are a starting point, not a converged design. Tuning
them is the open part of this week's work, the plan is to train, watch what the
agent actually does, and adjust one number at a time.

Things to try:
- If the agent stands still, the step penalty is too small relative to the risk
  of moving.
- If it dies every episode, it is running into its own trail, shorten the
  episode or increase the death penalty.
- If training is slow, drop to a 10×10 grid and 100k timesteps while iterating.

## Known Limitation

The win condition depends on who has more territory **when time runs out**, but
the number of steps remaining is not part of the observation. The agent is
racing a clock it cannot see. Rewarding the change in the territory gap on every
step sidesteps most of this, the agent is pushed to stay ahead continuously
rather than to time a final push, but adding remaining time to the observation
would make the problem properly Markov.
