# Week 1 — Python Fundamentals & Grid Simulation

## Overview
Week 1 focused on building the foundational Python skills needed for the rest of the project, classes, modules, and basic terminal I/O - by implementing a simple grid-based simulation from scratch. The goal was a 3×10 board where a player moves under keyboard input, respecting boundaries and obstacles. This is the base layer every later week (Pygame rendering, territory capture, RL environments) builds on top of.

## Topics Covered
- Representing a 2D grid as a list of lists in Python
- Encoding game entities as simple characters (`P` = player, `X` = obstacle, `.` = empty)
- Reading and validating keyboard input (`W A S D`) in a terminal loop
- Boundary checking (preventing the player index from leaving the grid)
- Separating concerns across files: `constants.py` (config), `utils.py` (grid/movement logic), `main.py` (game loop)

## Assignment
Build a simple grid-based simulation where a player moves inside a 2D board:
- Create a 3×10 grid
- Represent the player using `P`
- Take movement input using `W A S D` and update the player's position accordingly
- Prevent the player from leaving the grid; print `"Invalid Move"` on an invalid move
- Add at least 5 obstacle cells (`X`) that block movement

## Key Results
- Grid renders correctly as a 3×10 board with 5 obstacles placed on the corners/edges
- Player moves in all four directions and the grid updates in place each turn
- Moves into a wall (out-of-bounds) or into an obstacle are both correctly rejected with `"Invalid Move"`, without crashing or moving the player
- Any non-WASD key input is also caught and rejected the same way

## Reflection Questions
**1. Why separate `constants.py`, `utils.py`, and `main.py` instead of one file?**
It keeps configuration (grid size, symbols) independent of logic (movement, rendering) and independent of the control flow (the game loop). This makes Week 2 easy — the constants and movement logic can be swapped for a Pygame version without rewriting everything.

**2. What's the difference between "out of bounds" and "blocked by obstacle" in the code?**
Both must be checked before actually moving the player. Out-of-bounds is a check on the *new* row/column against grid dimensions; obstacle-blocking is a check on the *content* of the target cell. Both must fail closed - the player's position only updates if neither check trips.

**3. Why update the grid by clearing the old cell before setting the new one?**
If the new cell is written first, the old cell would still show a duplicate `P` until cleared, and more importantly, if the move is later found invalid, the grid should never be mutated at all. Validity must be resolved before any mutation happens.

## Conclusion & Next Steps
Week 1 established the basic simulation loop and grid representation used throughout the project. 
Week 2 upgrades this into a real-time, graphical, two-player game using Pygame, the same grid/movement ideas carry over, just rendered visually and driven by a game loop instead of `input()`.
