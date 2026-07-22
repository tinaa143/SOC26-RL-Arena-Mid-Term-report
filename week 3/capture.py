import numpy as np

from utils import inside_grid


def capture_territory(grid, player, rows, cols):
    # The trail becomes territory first, so it forms part of the enclosing wall.
    for pos in player.trail:
        grid[pos] = player.number

    # Flood inward from the border. Anything the flood reaches is outside the loop.
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

        if not inside_grid(row, col, rows, cols):
            continue
        if outside[row][col]:
            continue
        if grid[row][col] == player.number:
            continue

        outside[row][col] = True
        stack.append((row + 1, col))
        stack.append((row - 1, col))
        stack.append((row, col + 1))
        stack.append((row, col - 1))

    # Any empty cell the flood could not reach is enclosed, so it is captured.
    grid[(grid == 0) & ~outside] = player.number

    player.trail = []
    player.on_territory = True
