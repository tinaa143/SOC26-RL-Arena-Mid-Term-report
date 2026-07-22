# Week 5 — RL Environment Design & Training

Building a custom Gymnasium environment and training an agent on it with PPO.

## How to Run

```
pip install -r requirements.txt
python3 cartpole.py        # warmup: a pre-built environment
python3 maze_train.py      # train the maze agent, saves maze_ppo.zip
python3 maze.py            # watch the trained agent solve the maze
```

## Task 1 — CartPole

Provided by the mentor and run unchanged. It creates `CartPole-v1`, trains PPO
for 50,000 timesteps, then runs the trained policy with
`model.predict(obs, deterministic=True)`, resetting whenever the episode ends.
This is the whole Gymnasium interaction loop in about twelve lines.

## Task 2 — Maze

A 10×10 maze with walls (1) and open paths (0). The agent starts at (1, 1) and
must reach the goal at (8, 8). The shortest path is **14 steps**.

### Environment

| Piece | Choice |
|---|---|
| Action space | `Discrete(4)` — up, right, down, left |
| Observation space | `Box(0, 1, (1, 10, 10), float32)` |
| Episode limit | 200 steps, then truncated |

### Observation

The maze and the agent are encoded into one channel as `0` path, `1` wall,
`2` goal, `3` agent, then divided by 3 to land in `[0, 1]`.

`float32` normalised to `[0, 1]` is used rather than raw `int8` values 0–3.
Neural networks expect well-scaled float inputs; raw integers produce large
gradients and make training slow or unstable.

### Rewards

| Event | Value |
|---|---|
| Reaching the goal | `+10.0` |
| Bumping a wall (and not moving) | `-0.5` |
| Every step | `-0.01` |
| Re-entering an already visited cell | `-0.3` |

The goal reward is `+10` rather than `+1`. With a 200-step limit and a per-step
cost, a `+1` goal is a weak signal compared to the accumulated penalties along
the way, and the agent has little reason to prefer finishing over wandering.

### Training

```python
PPO("MlpPolicy", env, n_steps=1024, batch_size=64, ent_coef=0.01)
model.learn(total_timesteps=200_000)
```

`ent_coef=0.01` matters. PPO defaults to `ent_coef=0`, which applies no
exploration pressure at all, and the agent tends to settle into standing still
against a wall rather than searching.

`total_timesteps` is 200,000 rather than the 50,000 in the starter file, because
50,000 is not enough for this maze to converge.

### Result

After 200,000 timesteps the agent solves the maze in **14 steps** - the proven
shortest path, on every evaluation episode.

## Note on `check_env` warnings

`stable_baselines3.common.env_checker.check_env` prints three warnings about the
observation looking like an image with the wrong dtype and resolution. They are
expected and harmless here: the shape `(1, 10, 10)` is the one specified in the
assignment, and `MlpPolicy` flattens the observation rather than passing it to a
CNN, so the image-specific advice does not apply.

## Known Limitation

The revisit penalty depends on which cells have already been visited, but the
visited set is not part of the observation. Strictly, this makes the environment
partially observed, the agent cannot tell a fresh cell from a repeated one.
It still learns the maze because the layout is fixed, but adding a "visited"
channel to the observation would make the problem properly Markov.
