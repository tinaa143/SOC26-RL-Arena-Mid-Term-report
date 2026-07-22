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
- Touching the enemy **trail** kills the enemy and frees its territory — the
  agent wins and the episode ends.
- Touching the agent's **own** trail kills the agent.
- Leaving the grid kills the agent.
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
entirely. But touching your own trail is fatal, so an agent that cannot see it is
being asked to avoid something invisible. That makes the environment partially
observed in a way no amount of reward tuning can fix — the agent has no signal to
learn from. Adding the trail at `0.5` in channel 0 keeps the observation at three
channels while making every fatal cell visible.

### Grid vs Observation

The **grid** is the game logic — signed integers. The **observation** is what the
agent sees — three channels of floats in `[0, 1]`. `_get_obs()` converts one to
the other.

## Rewards

| Event | Value |
|---|---|
| Every step | `-0.02` |
| Every step spent outside your own territory | `-0.03` extra |
| Change in (my cells − enemy cells) | `× 1.0` |
| Killing the enemy | `+10.0`, episode ends |
| Dying — own trail or leaving the grid | `-3.0`, episode ends |
| Time out with more territory | `+5.0` |
| Time out with less territory | `-5.0` |

The territory reward is based on the **change in the gap**, not on the agent's own
count. Capturing ten tiles is worth nothing if the enemy still has twenty, so
rewarding the difference expresses the actual win condition directly. It also
handles the kill cleanly: when the enemy dies its territory drops to zero and the
gap widens on its own.

The per-step cost is a **penalty** rather than a survival bonus. With a discount
factor close to 1, any positive reward for merely staying alive makes an endless
safe loop more valuable than a risky capture, and the agent learns to stand still.

## Results

Trained with PPO (`MlpPolicy`, `n_steps=2048`, `batch_size=64`, `ent_coef=0.01`).
Evaluated on 150 unseen episodes with random enemy placement.

| Version | Kills | Deaths | Wins | Mean territory | Max |
|---|---|---|---|---|---|
| Grid edge blocks the agent, 300k | 18% | 2% | 18% | 9.0 | 9 |
| Grid edge is fatal, 120k | 27% | 50% | 27% | 9.6 | 79 |
| Grid edge is fatal, 300k | 43% | 34% | 43% | 9.0 | 9 |

### What the first version got wrong

Treating the grid edge as a block rather than a death was carried over from
Week 3, and it made a wall a permanently safe square. Tracing the trained agent
showed it walking in a straight line into a wall and parking there for the rest
of the episode — 200 steps across only 12 distinct cells. It never died and never
captured anything.

No reward tuning fixes this, because parking really was the optimal policy for
that environment. Making the edge fatal removed the safe square, and the agent
immediately started capturing, reaching 79 cells in its best episode.

### What the current version gets wrong

With longer training the agent converges on hunting the enemy trail and stops
capturing altogether. This is also rational: a kill pays `+10` **and** ends the
episode, avoiding every remaining step penalty, while a four-cell capture pays
`+4` and leaves the agent exposed. It is optimising the reward function as
written.

The next thing to try is lowering `KILL_REWARD` to around `3.0`, or not
terminating the episode on a kill so the agent still has to build territory
afterwards. Either change removes the incentive to end episodes as fast as
possible.

## Known Limitation

The win condition depends on who has more territory **when time runs out**, but
the number of steps remaining is not part of the observation. The agent is racing
a clock it cannot see. Rewarding the change in the territory gap on every step
sidesteps most of this, the agent is pushed to stay ahead continuously rather
than to time a final push, but adding remaining time to the observation would
make the problem properly Markov.
