from utils import inside_grid


def capture_territory(grid, player, rows, cols):
    # First convert the trail into normal territory.
    for pos in player.trail:
        grid[pos] = player.number

    outside = set()
    stack = []

    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                if grid[r][c] != player.number:
                    stack.append((r, c))

    while stack:
        row, col = stack.pop()

        if not inside_grid(row, col, rows, cols):
            continue
        if (row, col) in outside:
            continue
        if grid[row][col] == player.number:
            continue

        outside.add((row, col))
        stack.append((row + 1, col))
        stack.append((row - 1, col))
        stack.append((row, col + 1))
        stack.append((row, col - 1))

    # Any empty cell that cannot reach the border is inside the loop.
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0 and (r, c) not in outside:
                grid[r][c] = player.number

    player.trail = []
    player.on_territory = True
