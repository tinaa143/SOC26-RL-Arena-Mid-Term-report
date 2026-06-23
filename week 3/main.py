import pygame

from constants import *
from game import Game
from player import Player
from renderer import draw_game, draw_grid, draw_text

START_SCREEN = "start"
PLAYING = "playing"
GAME_OVER = "game_over"


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RL Arena")
clock = pygame.time.Clock()

red_player = Player(10, 10, RED, 1)
blue_player = Player(70, 70, BLUE, 2)
game = Game(ROWS, COLS)
game.add_player(red_player)
game.add_player(blue_player)

running = True
game_state = START_SCREEN


def handle_controls(keys):
    if keys[pygame.K_w]:
        red_player.dir = (-1, 0)
    elif keys[pygame.K_s]:
        red_player.dir = (1, 0)
    elif keys[pygame.K_a]:
        red_player.dir = (0, -1)
    elif keys[pygame.K_d]:
        red_player.dir = (0, 1)

    if keys[pygame.K_UP]:
        blue_player.dir = (-1, 0)
    elif keys[pygame.K_DOWN]:
        blue_player.dir = (1, 0)
    elif keys[pygame.K_LEFT]:
        blue_player.dir = (0, -1)
    elif keys[pygame.K_RIGHT]:
        blue_player.dir = (0, 1)


def draw_start_screen():
    screen.fill(BACKGROUND_COLOR)
    draw_grid(screen)
    draw_text(screen, "RL Arena ", 96, TITLE_COLOR, HEIGHT // 2 - 70)
    draw_text(screen, "Press SPACE to start", 40, MESSAGE_COLOR, HEIGHT // 2 + 20)


def draw_game_over_screen():
    draw_game(screen, game)
    draw_text(screen, "GAME OVER", 72, GAME_OVER_COLOR, HEIGHT // 2 - 20)
    draw_text(screen, "Press SPACE", 34, SOFT_WHITE, HEIGHT // 2 + 40)

while running:
    clock.tick(FPS)

    # handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_state == START_SCREEN:
                game.reset()
                game_state = PLAYING
            elif game_state == GAME_OVER:
                game.reset()
                game_state = START_SCREEN

    keys = pygame.key.get_pressed()

    if game_state == PLAYING:
        handle_controls(keys)
        game.update()

        if not red_player.alive or not blue_player.alive:
            game_state = GAME_OVER

    if game_state == START_SCREEN:
        draw_start_screen()
    elif game_state == PLAYING:
        draw_game(screen, game)
    elif game_state == GAME_OVER:
        draw_game_over_screen()

    pygame.display.update()

pygame.quit()
