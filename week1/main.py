from utils import *
from constants import *

grid = create_grid()
player_row = 0
player_col = 0
grid[0][0] = PLAYER

while True:
    display_grid(grid)
    direction = input("Enter move (W/A/S/D): ")
    if direction == "W" or direction == "A" or direction == "S" or direction == "D" or direction == "w" or direction == "a" or direction == "s" or direction == "d":
        player_row, player_col = move_player(grid, player_row, player_col, direction)
    else:
        print("Invalid Move")