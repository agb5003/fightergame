'''
FIGHTER GAME
Maximilian Fernaldy
Spring 2024
Computer Seminar I final project
'''

import sys
import random
import pygame
from entities import Enemy, Player
from game_management import Map, Level
from ui_elements import HealthBar, Menu

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Window:
    def __init__(self, dimensions, window_title):
        self.screen = pygame.display.set_mode((dimensions[0], dimensions[1]))
        pygame.display.set_caption(window_title)
        self.traversable_rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])

def quit_game():
    pygame.quit()
    sys.exit()

game_window = Window((1280, 720), "Fighter Game")

def main():
    clock = pygame.time.Clock()
    frames_per_second = 30

    level = Level(Map("./resources/preview_stage.png"),
    player_health=100, player_initial_position=(40, 200), enemies=[
        Enemy((40, 150), 5),
        Enemy((80, 250), 5),
        Enemy((10, 350), 5),
        Enemy((20, 580), 5),
        Enemy((340, 350), 5)
    ],
    )

    pause_menu_items = [Menu.MenuItems("./resources/UI/restart.png", (640, 360), level.start_from_beginning),
                        Menu.MenuItems("./resources/UI/quit.png", (640, 500), quit_game)]
    pause_menu = Menu(game_window.screen, "./resources/UI/pause_menu.png", pause_menu_items)

    game_over_menu_items = []
    game_over_menu = Menu(game_window.screen, "./resources/UI/game_over.png", game_over_menu_items)

    level.start_from_beginning()

    while True:
        clock.tick(frames_per_second)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level.game_state = "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if level.game_state == "play":
                        level.game_state = "pause"
                    elif level.game_state == "pause":
                        level.game_state = "play"

                if event.key == pygame.K_w:
                    level.player.up_pressed = True
                if event.key == pygame.K_a:
                    level.player.left_pressed = True
                if event.key == pygame.K_s:
                    level.player.down_pressed = True
                if event.key == pygame.K_d:
                    level.player.right_pressed = True

                if event.key == pygame.K_j:
                    level.player.lt_atk_pressed = True
                if event.key == pygame.K_k:
                    level.player.hv_atk_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    level.player.up_pressed = False
                if event.key == pygame.K_a:
                    level.player.left_pressed = False
                if event.key == pygame.K_s:
                    level.player.down_pressed = False
                if event.key == pygame.K_d:
                    level.player.right_pressed = False

                if event.key == pygame.K_j:
                    level.player.lt_atk_pressed = False
                if event.key == pygame.K_k:
                    level.player.hv_atk_pressed = False
        if level.game_state == "quit":
            quit_game()
            break

        if level.game_state == "game over":
            game_over_menu.update()
        elif level.game_state == "play":
            level.update(game_window)
            if level.player.health <= 0:
                print("game over")
                level.game_state = "game over"
        elif level.game_state == "pause":
            pause_menu.update()

if __name__ == "__main__":
    main()
