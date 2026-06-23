import numpy as np

from capture import capture_territory
from constants import START_TERRITORY_RADIUS
from utils import inside_grid


class Game:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        self._fill_start_territory(player)

    def update(self):
        for player in self.players:
            if player.alive:
                self._move_player(player)

    def reset(self):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        for player in self.players:
            player.reset()
            self._fill_start_territory(player)

    def _fill_start_territory(self, player):
        row, col = player.pos
        row_start = max(0, row - START_TERRITORY_RADIUS)
        row_end = min(self.rows, row + START_TERRITORY_RADIUS + 1)
        col_start = max(0, col - START_TERRITORY_RADIUS)
        col_end = min(self.cols, col + START_TERRITORY_RADIUS + 1)
        self.grid[row_start:row_end, col_start:col_end] = player.number

    def _move_player(self, player):
        next_row = player.pos[0] + player.dir[0]
        next_col = player.pos[1] + player.dir[1]

        if not inside_grid(next_row, next_col, self.rows, self.cols):
            return

        next_pos = (next_row, next_col)
        next_cell = self.grid[next_pos]

        if next_cell == -player.number:
            self._eliminate_player(player.number)
            return

        if next_cell < 0 and next_cell != -player.number:
            self._eliminate_player(-next_cell)
            self.grid[next_pos] = 0
        elif next_cell > 0 and next_cell != player.number:
            return

        if not player.on_territory:
            self.grid[player.pos] = -player.number
            player.trail.append(player.pos)

        player.pos = next_pos

        if self.grid[player.pos] == player.number:
            player.on_territory = True
            if player.trail:
                capture_territory(self.grid, player, self.rows, self.cols)
        else:
            player.on_territory = False

    def _eliminate_player(self, player_number):
        for player in self.players:
            if player.number == player_number:
                player.alive = False

                for pos in player.trail:
                    if self.grid[pos] == -player.number:
                        self.grid[pos] = 0

                player.trail = []
                return
