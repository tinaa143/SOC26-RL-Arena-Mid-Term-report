import pygame
from constants import *
from player import Player
from game import Game
from renderer import *

START_SCREEN = "start"
PLAYING = "playing"
GAME_OVER = "game_over"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RL Arena")
clock = pygame.time.Clock()

player1 = Player(5, 5, RED)
player2 = Player(15, 15, BLUE)
game = Game(ROWS, COLS)
game.add_player(player1)
game.add_player(player2)

running = True
game_state = START_SCREEN


def handle_controls(keys):
    if keys[pygame.K_w]:
        player1.dir = (-1, 0)
    elif keys[pygame.K_s]:
        player1.dir = (1, 0)
    elif keys[pygame.K_a]:
        player1.dir = (0, -1)
    elif keys[pygame.K_d]:
        player1.dir = (0, 1)

    if keys[pygame.K_UP]:
        player2.dir = (-1, 0)
    elif keys[pygame.K_DOWN]:
        player2.dir = (1, 0)
    elif keys[pygame.K_LEFT]:
        player2.dir = (0, -1)
    elif keys[pygame.K_RIGHT]:
        player2.dir = (0, 1)


def draw_start_screen():
    screen.fill(BACKGROUND_COLOR)
    draw_grid(screen)
    draw_text(screen, "RL Arena", 96, TITLE_COLOR, HEIGHT // 2 - 70)
    draw_text(screen, "Press SPACE to start", 40, MESSAGE_COLOR, HEIGHT // 2 + 20)


def draw_game_screen():
    screen.fill(BACKGROUND_COLOR)
    draw_grid(screen)

    for player in game.players:
        draw_trail(screen, player)

    for player in game.players:
        draw_player(screen, player)


def draw_game_over_screen():
    draw_game_screen()
    draw_text(screen, "GAME OVER", 72, GAME_OVER_COLOR, HEIGHT // 2 - 20)
    draw_text(screen, "Press SPACE", 34, SOFT_WHITE, HEIGHT // 2 + 40)


while running:
    clock.tick(FPS)

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

        if not player1.alive or not player2.alive:
            game_state = GAME_OVER

    if game_state == START_SCREEN:
        draw_start_screen()
    elif game_state == PLAYING:
        draw_game_screen()
    elif game_state == GAME_OVER:
        draw_game_over_screen()

    pygame.display.update()

pygame.quit()
