import numpy as np
import gymnasium as gym


GRID_SIZE = 15
MAX_STEPS = 200

AGENT = 1
ENEMY = 2

START_TERRITORY_RADIUS = 1        # 3x3 starting block for both sides
ENEMY_TRAIL_LENGTH = 5

# Action index -> (row change, column change)
ACTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]      # up, right, down, left

# Reward values - these are the numbers to experiment with.
STEP_PENALTY = -0.01       # small cost per step, so standing still is not free
DIFF_SCALE = 0.2           # reward per unit change in (my cells - enemy cells)
KILL_REWARD = 10.0         # touching the enemy trail
DEATH_PENALTY = -10.0      # touching your own trail
WIN_BONUS = 5.0            # more territory than the enemy when time runs out
LOSS_PENALTY = -5.0        # less territory than the enemy when time runs out

# Colours used by render()
COLOR_EMPTY = (18, 20, 26)
COLOR_AGENT_TERRITORY = (255, 80, 80)
COLOR_AGENT_TRAIL = (110, 30, 30)
COLOR_ENEMY_TERRITORY = (80, 160, 255)
COLOR_ENEMY_TRAIL = (25, 55, 110)
COLOR_AGENT_HEAD = (255, 255, 255)


def capture_territory(grid, trail, player_number):
    """Flood fill inward from the border - anything unreachable is enclosed."""
    rows, cols = grid.shape

    # The trail becomes territory first, so it forms part of the enclosing wall.
    for pos in trail:
        grid[pos] = player_number

    outside = np.zeros((rows, cols), dtype=bool)
    stack = []

    for col in range(cols):
        stack.append((0, col))
        stack.append((rows - 1, col))

    for row in range(rows):
        stack.append((row, 0))
        stack.append((row, cols - 1))

    while stack:
        row, col = stack.pop()

        if not (0 <= row < rows and 0 <= col < cols):
            continue
        if outside[row][col]:
            continue
        if grid[row][col] == player_number:
            continue

        outside[row][col] = True
        stack.append((row + 1, col))
        stack.append((row - 1, col))
        stack.append((row, col + 1))
        stack.append((row, col - 1))

    # Any empty cell the flood could not reach is enclosed, so it is captured.
    enclosed = (grid == 0) & ~outside
    grid[enclosed] = player_number

    return int(np.count_nonzero(enclosed)) + len(trail)


class RL_Arena_Env(gym.Env):
    """Single-agent Paper.io against a static enemy.

    Grid encoding (game logic):
        0   empty
       +1   agent territory      -1   agent trail
       +2   enemy territory      -2   enemy trail
    """

    metadata = {"render_modes": ["rgb_array"], "render_fps": 10}

    def __init__(self, grid_size=GRID_SIZE, max_steps=MAX_STEPS):
        super().__init__()

        self.grid_size = grid_size
        self.max_steps = max_steps

        self.observation_space = gym.spaces.Box(
            low=0.0, high=1.0, shape=(grid_size, grid_size, 3), dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(4)

        self.grid = np.zeros((grid_size, grid_size), dtype=np.int8)
        self.agent_pos = (0, 0)
        self.agent_trail = []
        self.on_territory = True
        self.enemy_alive = True
        self._steps = 0
        self._prev_diff = 0

    # -- setup ------------------------------------------------------------

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=np.int8)
        self.agent_trail = []
        self.on_territory = True
        self.enemy_alive = True
        self._steps = 0

        # The enemy is placed randomly every episode so the agent has to look
        # for it rather than memorise one route.
        enemy_pos = self._random_spawn()
        self._fill_territory(enemy_pos, ENEMY)
        self._place_enemy_trail(enemy_pos)

        # The agent spawns somewhere that does not touch the enemy at all.
        self.agent_pos = self._free_spawn()
        self._fill_territory(self.agent_pos, AGENT)

        self._prev_diff = self._territory_diff()

        return self._get_obs(), {}

    def _random_spawn(self):
        low = START_TERRITORY_RADIUS
        high = self.grid_size - START_TERRITORY_RADIUS - 1
        return (int(self.np_random.integers(low, high + 1)),
                int(self.np_random.integers(low, high + 1)))

    def _free_spawn(self):
        low = START_TERRITORY_RADIUS
        high = self.grid_size - START_TERRITORY_RADIUS - 1
        candidates = [(row, col)
                      for row in range(low, high + 1)
                      for col in range(low, high + 1)
                      if self._area_is_empty((row, col))]
        return candidates[int(self.np_random.integers(len(candidates)))]

    def _fill_territory(self, pos, number):
        row, col = pos
        r0 = max(0, row - START_TERRITORY_RADIUS)
        r1 = min(self.grid_size, row + START_TERRITORY_RADIUS + 1)
        c0 = max(0, col - START_TERRITORY_RADIUS)
        c1 = min(self.grid_size, col + START_TERRITORY_RADIUS + 1)
        self.grid[r0:r1, c0:c1] = number

    def _area_is_empty(self, pos):
        row, col = pos
        r0 = max(0, row - START_TERRITORY_RADIUS - 1)
        r1 = min(self.grid_size, row + START_TERRITORY_RADIUS + 2)
        c0 = max(0, col - START_TERRITORY_RADIUS - 1)
        c1 = min(self.grid_size, col + START_TERRITORY_RADIUS + 2)
        return bool(np.all(self.grid[r0:r1, c0:c1] == 0))

    def _place_enemy_trail(self, enemy_pos):
        """Lay a short trail leading away from the enemy territory.

        Directions are tried in random order and the first one with enough
        room for the whole trail is used, so the trail is never cut short.
        """
        row, col = enemy_pos
        order = list(range(4))
        self.np_random.shuffle(order)

        for index in order:
            direction = ACTIONS[index]
            start = (row + direction[0] * (START_TERRITORY_RADIUS + 1),
                     col + direction[1] * (START_TERRITORY_RADIUS + 1))
            end = (start[0] + direction[0] * (ENEMY_TRAIL_LENGTH - 1),
                   start[1] + direction[1] * (ENEMY_TRAIL_LENGTH - 1))

            if not (self._inside(start) and self._inside(end)):
                continue

            cell = start
            for _ in range(ENEMY_TRAIL_LENGTH):
                self.grid[cell] = -ENEMY
                cell = (cell[0] + direction[0], cell[1] + direction[1])
            return

    # -- stepping ---------------------------------------------------------

    def step(self, action):
        self._steps += 1
        reward = STEP_PENALTY
        terminated = False

        row_change, col_change = ACTIONS[int(action)]
        next_pos = (self.agent_pos[0] + row_change,
                    self.agent_pos[1] + col_change)

        blocked = False

        if not self._inside(next_pos):
            # The grid edge blocks the agent, it does not kill it.
            blocked = True
        else:
            next_cell = self.grid[next_pos]

            if next_cell == -AGENT:
                # Your own trail kills you.
                reward += DEATH_PENALTY
                return self._get_obs(), reward, True, False, {"result": "dead"}

            if next_cell == -ENEMY:
                # Touching the enemy trail kills the enemy and frees its land.
                self._kill_enemy()
                reward += KILL_REWARD
                terminated = True

            elif next_cell == ENEMY:
                # Enemy territory blocks the agent.
                blocked = True

        if not blocked:
            # The trail is left on the cell being vacated, not the one entered.
            if not self.on_territory:
                self.grid[self.agent_pos] = -AGENT
                self.agent_trail.append(self.agent_pos)

            self.agent_pos = next_pos

            if self.grid[self.agent_pos] == AGENT:
                self.on_territory = True
                if self.agent_trail:
                    capture_territory(self.grid, self.agent_trail, AGENT)
                    self.agent_trail = []
            else:
                self.on_territory = False

        # Reward the CHANGE in the territory gap, so growing your own area only
        # counts insofar as it puts you ahead of the enemy.
        diff = self._territory_diff()
        reward += DIFF_SCALE * (diff - self._prev_diff)
        self._prev_diff = diff

        truncated = False
        if not terminated and self._steps >= self.max_steps:
            truncated = True
            reward += WIN_BONUS if diff > 0 else LOSS_PENALTY

        info = {"result": "killed_enemy" if terminated else ""}
        return self._get_obs(), reward, terminated, truncated, info

    def _kill_enemy(self):
        self.enemy_alive = False
        self.grid[self.grid == ENEMY] = 0
        self.grid[self.grid == -ENEMY] = 0

    def _territory_diff(self):
        mine = int(np.count_nonzero(self.grid == AGENT))
        theirs = int(np.count_nonzero(self.grid == ENEMY))
        return mine - theirs

    def _inside(self, pos):
        row, col = pos
        return 0 <= row < self.grid_size and 0 <= col < self.grid_size

    # -- observation ------------------------------------------------------

    def _get_obs(self):
        obs = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.float32)

        # Channel 0 - your own stuff.
        obs[:, :, 0][self.grid == AGENT] = 1.0
        obs[:, :, 0][self.grid == -AGENT] = 0.5

        # Channel 1 - enemy territory, which blocks you.
        obs[:, :, 1][self.grid == ENEMY] = 1.0

        # Channel 2 - enemy trail, which is killable, plus your own head.
        obs[:, :, 2][self.grid == -ENEMY] = 1.0
        obs[:, :, 2][self.agent_pos] = 0.5

        return obs

    # -- rendering --------------------------------------------------------

    def render(self):
        return self._render_rgb()

    def _render_rgb(self):
        rgb = np.zeros((self.grid_size, self.grid_size, 3), dtype=np.uint8)

        rgb[self.grid == 0] = COLOR_EMPTY
        rgb[self.grid == AGENT] = COLOR_AGENT_TERRITORY
        rgb[self.grid == -AGENT] = COLOR_AGENT_TRAIL
        rgb[self.grid == ENEMY] = COLOR_ENEMY_TERRITORY
        rgb[self.grid == -ENEMY] = COLOR_ENEMY_TRAIL
        rgb[self.agent_pos] = COLOR_AGENT_HEAD

        return rgb
