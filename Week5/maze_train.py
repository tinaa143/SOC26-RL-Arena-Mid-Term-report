import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO


# 1 = wall, 0 = open path
MAZE = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
], dtype=np.int8)

START_POS = (1, 1)
GOAL_POS = (8, 8)

# Action index -> (row change, column change)
ACTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]   # up, right, down, left

# Cell codes used inside the observation, before normalisation.
PATH, WALL, GOAL, AGENT = 0, 1, 2, 3
MAX_CELL_VALUE = 3

# Reward values - these are the numbers worth experimenting with.
GOAL_REWARD = 10.0
WALL_PENALTY = -0.5
STEP_PENALTY = -0.01
REVISIT_PENALTY = -0.3


class MazeEnv(gym.Env):
    metadata = {"render_modes": ["rgb_array"], "render_fps": 10}

    def __init__(self, max_steps=200):
        super().__init__()

        self.action_space = spaces.Discrete(4)

        # float32 in [0, 1] rather than raw int 0-3. Neural networks expect
        # well-scaled float inputs; raw integers produce large gradients and
        # slow or unstable learning.
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(1, 10, 10), dtype=np.float32
        )

        self._maze = MAZE
        self.rows, self.cols = self._maze.shape
        self.start_pos = START_POS
        self.goal_pos = GOAL_POS

        self._max_steps = max_steps
        self._steps = 0
        self.agent_pos = self.start_pos
        self._visited = set()

    def _get_obs(self):
        obs = np.zeros((1, self.rows, self.cols), dtype=np.float32)

        obs[0][self._maze == 1] = WALL
        obs[0][self.goal_pos] = GOAL
        obs[0][self.agent_pos] = AGENT

        # Normalise to [0, 1] so the network sees well-scaled inputs.
        return obs / MAX_CELL_VALUE

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.agent_pos = self.start_pos
        self._steps = 0
        self._visited = {self.start_pos}

        return self._get_obs(), {}

    def step(self, action):
        self._steps += 1

        row_change, col_change = ACTIONS[int(action)]
        next_pos = (self.agent_pos[0] + row_change,
                    self.agent_pos[1] + col_change)

        reward = STEP_PENALTY

        if self._is_wall(next_pos):
            # Bumping a wall costs something, and the agent does not move.
            reward += WALL_PENALTY
        else:
            self.agent_pos = next_pos

            if next_pos in self._visited:
                reward += REVISIT_PENALTY
            self._visited.add(next_pos)

        terminated = self.agent_pos == self.goal_pos
        if terminated:
            reward += GOAL_REWARD

        # End the episode if the agent has not solved the maze in time.
        truncated = (not terminated) and (self._steps >= self._max_steps)

        return self._get_obs(), reward, terminated, truncated, {}

    def render(self):
        return self._render_rgb()

    def _render_rgb(self):
        rgb = np.zeros((self.rows, self.cols, 3), dtype=np.uint8)

        rgb[self._maze == 0] = (235, 240, 245)     # open path
        rgb[self._maze == 1] = (35, 40, 50)        # wall
        rgb[self.goal_pos] = (80, 220, 120)        # goal
        rgb[self.agent_pos] = (255, 80, 80)        # agent

        return rgb

    def _is_wall(self, pos):
        row, col = pos
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return True
        return self._maze[row][col] == 1


def main():
    env = MazeEnv()

    # ent_coef=0.01 adds exploration pressure. PPO's default of 0 gives none,
    # and the agent can settle into standing still in a corner.
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        n_steps=1024,
        batch_size=64,
        ent_coef=0.01,
    )
    model.learn(total_timesteps=200_000)
    model.save("maze_ppo")


if __name__ == "__main__":
    main()
