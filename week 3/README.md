# Week 3 — Paper.io Territory Capture

Week 2's Tron game extended with Paper.io style territory capture.
Each player owns a territory, leaves a trail when they step outside it, and
captures everything enclosed when they reconnect.

## How to Run

```
pip install pygame numpy
cd "week 3"
python3 main.py
```

## Controls

- **Red:** W A S D
- **Blue:** Arrow keys
- **SPACE:** start / return to menu

## Rules

- Leave your territory and you start laying a trail
- Return to your own territory and the enclosed area is captured
- Touching **your own** trail kills you
- Touching the **opponent's** trail kills the opponent
- Head-on collision kills both players
- Opponent territory and the grid edge are **blocked**, not fatal — you stay
  put until you change direction

## Grid Encoding

A single integer per cell, so every collision check is one comparison:

```
 0   empty
+N   player N's territory
-N   player N's trail
```

## Files

| File | Role |
|---|---|
| `constants.py` | 800×800 screen, 80×80 grid, FPS 10, territory/trail colours |
| `player.py` | `Player` — pos, dir, trail, number, alive, `on_territory` |
| `game.py` | movement, collisions, trail placement, capture trigger |
| `capture.py` | flood-fill territory capture |
| `renderer.py` | grid → colour array → `blit_array`, player circles on top |
| `utils.py` | `inside_grid` bounds helper |
| `main.py` | game loop and START / PLAYING / GAME_OVER screens |

## Design Notes

- **Trail is placed on the cell being vacated**, not the cell being entered.
  Writing it at the current position would mean stepping onto your own trail
  and dying immediately.
- **Capture works by flooding inward from the edge.** The trail is converted to
  territory first so it acts as part of the wall, then a flood fill starts from
  every border cell and spreads through anything that isn't yours. Any empty
  cell the flood cannot reach is enclosed, so it becomes territory. This handles
  loops drawn against the grid edge correctly, which a naive fill does not.
- **Opponent territory does not block the flood**, so only your own trail and
  territory form the enclosing boundary. Capture converts empty cells only, so
  opponent territory caught inside a loop is left untouched.
- **Simultaneous movement.** `update()` runs in three phases: compute every
  intended position, resolve head-on collisions, then commit. Moving players one
  at a time would make the winner of a collision depend on list order rather
  than on the rules.
- **Rendering is vectorised.** The grid becomes an RGB array using boolean masks
  with no Python loops, is scaled with `np.repeat`, and is pushed in a single
  `pygame.surfarray.blit_array()` call. Trail colours are dimmed versions of the
  territory colours so the two are distinguishable at a glance.

## Not Implemented

Optional extras from the spec: capturing opponent territory, score display,
powerups.
