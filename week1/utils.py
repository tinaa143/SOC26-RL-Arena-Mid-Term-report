
from constants import *

def clear_screen():
    print("\n" * 40)


def print_grid(grid):
    for row in grid:
        print(" ".join(row))

def display_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end=" ")
        print()

def create_grid():
    grid = []
    for i in range(ROWS):
        row = [EMPTY] * COLS
        grid.append(row)
    
    grid[0][9] = OBSTACLE
    grid[1][0] = OBSTACLE
    grid[1][9] = OBSTACLE
    grid[2][0] = OBSTACLE
    grid[2][9] = OBSTACLE
    return grid

def move_player(grid, player_row, player_col, direction):
    new_row = player_row
    new_col = player_col

    if direction == "W" or direction == "w":
        new_row = player_row - 1
        
    elif direction == "S" or direction == "s":
        new_row = player_row + 1

    elif direction == "A" or direction == "a":
        new_col = player_col - 1

    elif direction == "D" or direction == "d" :
        new_col = player_col + 1

    if 0 <= new_row < ROWS and 0 <= new_col < COLS:
        if grid[new_row][new_col] != OBSTACLE:
            grid[player_row][player_col] = EMPTY
            grid[new_row][new_col] = PLAYER
            return new_row, new_col
        else:
            print("Invalid Move")
    else:
        print("Invalid Move")
    
    return player_row, player_col        
