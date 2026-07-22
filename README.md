# RL Arena

**Seasons of Code 2026 — PID 73**

A six-week project that starts with a player moving around a text grid in the
terminal and ends with a reinforcement learning agent playing Paper.io on its own.

Each week builds directly on the last. The grid from Week 1 becomes the Pygame
board in Week 2, which gains territory capture in Week 3, which becomes the
environment an agent is trained on in Week 6.

```
Week 1    terminal grid, WASD movement
   ↓
Week 2    Pygame, two players, Tron trails
   ↓
Week 3    territory capture with flood fill  ──────┐
                                                   │
Week 4    RL theory — MDPs, policies, value functions, PPO
   ↓                                               │
Week 5    custom Gymnasium environments, PPO training
   ↓                                               │
Week 6    the Week 3 game as a Gym environment  ←──┘
          + a trained agent
```

## Structure

```
WEEK-1/   terminal grid game
WEEK-2/   Tron-style two player game
WEEK-3/   Paper.io territory capture
WEEK-4/   reinforcement learning theory notes
WEEK-5/   Gymnasium environment design + PPO
WEEK-6/   RL Arena as a Gym environment + trained agent
```

Every week has its own `README.md` with the details, design decisions and
results for that week.

## Requirements

Python 3, plus:

| Package | Used from |
|---|---|
| `numpy` | Week 2 |
| `pygame` | Week 2 |
| `gymnasium` | Week 5 |
| `stable-baselines3` | Week 5 |

Weeks 5 and 6 each have a `requirements.txt`.

## Quick Start

```
# Week 1 — no dependencies
cd WEEK-1 && python3 main.py

# Weeks 2 and 3 — needs pygame and numpy
pip install pygame numpy
cd WEEK-2 && python3 main.py
cd WEEK-3 && python3 main.py

# Weeks 5 and 6 — needs the full stack
pip install -r WEEK-5/requirements.txt

cd WEEK-5 && python3 maze_train.py && python3 maze.py
cd WEEK-6 && python3 train.py      && python3 play.py
```

---

## Week 1 — Terminal Grid Game

A player moves on a 3×10 board using `W A S D`, with five obstacles blocking
movement and boundary checks preventing it from leaving the grid.

Split across `constants.py` (configuration), `utils.py` (grid and movement
logic) and `main.py` (the input loop), so the grid size and cell symbols can be
changed without touching any logic.

## Week 2 — Tron Style Two Player Game

Two players move continuously on an 80×80 grid inside an 800×800 Pygame window,
leaving permanent trails. A player dies on hitting a wall, hitting any trail, or
colliding head-on with the other player.

The interesting part is the update order. `Game.update()` computes every player's
next position first, resolves deaths, and only then commits the moves. Moving
players one at a time would let the second player crash into a trail the first
had only just created on the same tick. Player heads are written into the numpy
grid, which makes both same-cell and position-swap collisions fall out of a
single `grid[next_pos] != 0` check.

Controls: **Red** `W A S D`, **Blue** arrow keys, **SPACE** to start.

## Week 3 — Paper.io Territory Capture

Week 2 extended so each player owns a territory. Step outside it and you leave a
trail; return and everything enclosed by the trail and your border is captured.

- **Encoding** — one integer per cell: `0` empty, `+N` player N's territory,
  `-N` player N's trail. Every collision check is a single comparison.
- **Trail placement** — the trail goes on the cell being *vacated*, not the one
  being entered, otherwise you stand on your own trail and die immediately.
- **Capture** — the trail becomes territory first so it acts as a wall, then a
  flood fill runs inward from the grid border. Any empty cell the flood cannot
  reach is enclosed, so it is captured. This handles loops drawn against the grid
  edge, which a naive fill does not.
- **Rendering** — the grid is turned into an RGB array with numpy boolean masks
  and no Python loops, then pushed in a single `pygame.surfarray.blit_array()`
  call. Drawing 6400 rectangles individually is far too slow.

Collisions: your own trail kills you, the opponent's trail kills them, and
opponent territory or the grid edge blocks you without killing.

## Week 4 — Reinforcement Learning Theory

Notes covering the language and mathematics of RL: agents and environments,
states versus observations, action spaces, deterministic and stochastic
policies, trajectories, discounted return and the discount factor, value and
action-value functions, the optimal action, the Bellman equations, advantage
functions, and Markov Decision Processes.

The final section maps the Week 3 game onto the MDP tuple `⟨S, A, R, P, ρ0⟩`,
which is what the environment in Week 6 is built from.

## Week 5 — Environment Design and Training

Two tasks.

**CartPole** — a warm-up on a pre-built Gymnasium environment, training PPO and
running the trained policy.

**Maze** — a custom `gym.Env` for a 10×10 maze. The agent starts at `(1, 1)` and
must reach `(8, 8)`. Observations are a single `10×10` channel encoding path,
wall, goal and agent, normalised to `[0, 1]` because neural networks need
well-scaled float inputs. Rewards are `+10` for the goal, `-0.5` for bumping a
wall, `-0.01` per step and `-0.3` for revisiting a cell, with episodes truncated
at 200 steps.

**Result:** after 200,000 timesteps the agent solves the maze in **14 steps** —
the shortest path — on every evaluation episode.

## Week 6 — RL Arena as a Gym Environment

The Paper.io game turned into a Gymnasium environment: one agent against a static
enemy on a 15×15 grid, `Discrete(4)` actions and a `(15, 15, 3)` observation.
The agent wins by killing the enemy or by holding more territory when time runs
out. Enemy placement is randomised every episode.

**Results** — PPO, 150 unseen evaluation episodes:

| Version | Kills | Deaths | Wins | Mean territory | Max |
|---|---|---|---|---|---|
| Grid edge blocks the agent, 300k | 18% | 2% | 18% | 9.0 | 9 |
| Grid edge is fatal, 120k | 27% | 50% | 27% | 9.6 | 79 |
| Grid edge is fatal, 300k | 43% | 34% | 43% | 9.0 | 9 |

Both failure modes came from tracing what the agent actually did rather than
guessing at numbers.

In the first version the grid edge blocked the agent instead of killing it, which
made a wall a permanently safe square. The trained agent walked in a straight
line into a wall and parked there for the whole episode — 200 steps across 12
distinct cells, never dying, never capturing. No reward tuning fixes that,
because parking genuinely was optimal. Making the edge fatal removed the safe
square and the agent started capturing immediately.

In the current version the agent converges on hunting the enemy trail and stops
capturing, because a kill pays `+10` *and* ends the episode, dodging every
remaining step penalty, while a small capture pays little and leaves it exposed.
Lowering the kill reward, or not ending the episode on a kill, is the next thing
to try.

## Notes

- Weeks 1 to 3 are pure Python and Pygame with no machine learning.
- Week 4 is written notes only.
- Weeks 5 and 6 use Gymnasium and Stable-Baselines3.
- Week 6's observation includes the agent's own trail, which the original brief
  left out. Since touching that trail is fatal, an agent that cannot see it is
  being asked to avoid something invisible — a reward-tuning problem no amount of
  tuning can solve. The reasoning is written up in `WEEK-6/README.md`.
