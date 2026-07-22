# Week 2 — Tron Style Two Player Game

Week 1's terminal grid upgraded into a real-time graphical two-player game using Pygame.
Two players move continuously on an 80×80 grid leaving permanent trails behind them.

## How to Run

```
pip install pygame numpy
cd "week 2"
python3 main.py
```

## Controls

- **Red:** W A S D
- **Blue:** Arrow keys
- **SPACE:** start / return to menu

## Rules

- Both players move one cell every frame in their current direction
- You die on: hitting a wall, hitting any trail, or a head-on collision
- The game ends as soon as either player dies

## Files

| File | Role |
|---|---|
| `constants.py` | 800×800 screen, 80×80 grid, `CELL_SIZE = WIDTH // COLS`, FPS 10, colours |
| `player.py` | `Player` class — pos, dir, trail, colour, alive, `reset()` |
| `game.py` | grid state, movement, collision resolution |
| `renderer.py` | `draw_grid`, `draw_player`, `draw_trail`, `draw_text` |
| `main.py` | game loop with START / PLAYING / GAME_OVER screens |

## Design Notes

- **Simultaneous movement.** `Game.update()` computes every player's next position
  first, then resolves deaths, then commits the moves. Moving players one at a time
  would let the second player crash into a trail the first only just created on the
  same tick.
- **Head-on collisions** are caught two ways: two players targeting the same cell is
  checked explicitly, and a straight positional swap is caught because each player's
  head is written into the grid, so `grid[next_pos] != 0` trips for both.
- **Collision checks use the numpy grid** (`self.grid[next_pos] != 0`) rather than
  `next_pos in player.trail`, O(1) instead of O(trail length), which matters once
  trails reach thousands of cells.
- **Coordinate convention:** positions are `(row, col)` and directions are
  `(Δrow, Δcol)` throughout, matching `grid[row][col]`.

## Not Implemented

Optional extras from the spec: score system, fading trails.
