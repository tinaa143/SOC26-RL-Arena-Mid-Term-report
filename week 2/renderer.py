import pygame
from constants import *


def draw_grid(screen):
    for row in range(ROWS):
        pygame.draw.line(screen, GRID_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE))

    for col in range(COLS):
        pygame.draw.line(screen, GRID_COLOR, (col * CELL_SIZE, 0), (col * CELL_SIZE, HEIGHT))


def draw_player(screen, player):
    row, col = player.pos
    x = col * CELL_SIZE
    y = row * CELL_SIZE
    pygame.draw.rect(screen, player.color, (x, y, CELL_SIZE, CELL_SIZE))


def draw_trail(screen, player):
    for row, col in player.trail:
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        pygame.draw.rect(screen, player.color, (x, y, CELL_SIZE, CELL_SIZE))


def draw_text(screen, text, size, color, center_y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, center_y))
    screen.blit(text_surface, text_rect)
