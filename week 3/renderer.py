import pygame
import numpy as np

from constants import *


def draw_grid(screen):
    for row in range(ROWS):
        pygame.draw.line(screen, GRID_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE))

    for col in range(COLS):
        pygame.draw.line(screen, GRID_COLOR, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT))


def draw_text(screen, text, size, color, center_y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, center_y))
    screen.blit(text_surface, text_rect)


def draw_game(screen, game):
    color_grid = np.zeros((ROWS, COLS, 3), dtype=np.uint8)
    color_grid[game.grid == 0] = BLACK
    color_grid[game.grid == 1] = RED
    color_grid[game.grid == 2] = BLUE
    color_grid[game.grid == -1] = RED_TRAIL
    color_grid[game.grid == -2] = BLUE_TRAIL

    color_array = np.repeat(np.repeat(color_grid, CELL_SIZE, axis=0), CELL_SIZE, axis=1)
    pygame.surfarray.blit_array(screen, np.transpose(color_array, (1, 0, 2)))

    for player in game.players:
        if player.alive:
            row, col = player.pos
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, WHITE, (x, y), CELL_SIZE // 2)
