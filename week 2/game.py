import numpy as np


class Game:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols), dtype=int)
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        self.grid[player.pos] = 1

    def get_next_position(self, player):
        row, col = player.pos
        row_dir, col_dir = player.dir
        return (row + row_dir, col + col_dir)

    def is_outside_grid(self, pos):
        row, col = pos
        return row < 0 or row >= self.rows or col < 0 or col >= self.cols

    def update(self):
        crashed_players = set()
        moves = []

        for player in self.players:
            if not player.alive:
                continue

            next_pos = self.get_next_position(player)
            moves.append((player, next_pos))

        for player, next_pos in moves:
            if self.is_outside_grid(next_pos):
                crashed_players.add(player)
            elif self.grid[next_pos] != 0:
                crashed_players.add(player)

        for i in range(len(moves)):
            player1, next_pos1 = moves[i]
            for j in range(i + 1, len(moves)):
                player2, next_pos2 = moves[j]
                if next_pos1 == next_pos2:
                    crashed_players.add(player1)
                    crashed_players.add(player2)

        for player in crashed_players:
            player.alive = False

        for player, next_pos in moves:
            if player.alive:
                player.trail.append(player.pos)
                player.pos = next_pos
                self.grid[player.pos] = 1

    def reset(self):
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        for player in self.players:
            player.reset()
            self.grid[player.pos] = 1
