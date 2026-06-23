# SoC 2026 — RL Arena

## Week 1 — Text Based Grid Game
A simple terminal game where a player moves on a 3×10 grid.
- Movement using W A S D
- 5 obstacles placed on edges
- Boundary and obstacle checking
- Prints "Invalid Move" for blocked moves

## Week 2 — Tron Style Two Player Game
A graphical two player Tron game using pygame.
- 800×800 screen, 80×80 grid
- Two players leave trails behind
- Player dies on wall, trail, or head-on collision
- Player 1: WASD | Player 2: Arrow Keys

## Week 3 — Paper.io Territory Capture
Extended Week 2 with territory capture.
- Players capture area by enclosing it with their trail
- Flood Fill algorithm used for territory capture
- New collision rules: own trail = death, opponent trail = opponent dies, opponent territory = blocked
- Fast rendering using numpy and pygame.surfarray

## Week 4 — Reinforcement Learning Summary
Explored RL fundamentals through provided resources.
- Agent interacts with environment: State → Action → Reward → Next State
- Learned about Policies, Value Functions, Action Spaces
- Bellman Equations and Advantage Functions
- Goal: find optimal policy to maximize cumulative rewards

---


