'''
FIGHTER GAME
Maximilian Fernaldy
Spring 2024
Computer Seminar I final project
'''

import json
import sys
import pygame
from entities import Enemy
from game_manager import GameInstance, Map, Level
from ui_elements import Menu, RollingScreen

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def quit_game():
    pygame.quit()
    sys.exit()


# Level(Map("./resources/Miami-synth-files/Layers/highway.png", 3, pygame.Rect(0, 400, 2280, SCREEN_HEIGHT-400)),
# player_health=100, player_initial_position=(40, 400), enemies=[
#     Enemy((40, 450), 5),
#     Enemy((800, 350), 5),
#     Enemy((1000, 390), 5),
# ]),

def main():

    game_instance = GameInstance((1280, 720), "Sendai 11PM")

    clock = pygame.time.Clock()
    frames_per_second = 60

    start_menu_items = [Menu.MenuItemTextOnly("New Game", (640, 360), game_instance.start_next_stage)]
    start_menu = Menu(game_instance.screen, "./resources/UI/pause_menu.png", start_menu_items)

    continue_menu_items = [Menu.MenuItemTextOnly("Next level", (640, 360), game_instance.start_next_stage)]
    continue_menu = Menu(game_instance.screen, "./resources/UI/pause_menu.png", continue_menu_items)

    pause_menu_items = [Menu.MenuItem("./resources/UI/restart.png", (640, 360), game_instance.current_level.start_from_beginning),
                        Menu.MenuItem("./resources/UI/quit.png", (640, 500), quit_game)]
    pause_menu = Menu(game_instance.screen, "./resources/UI/pause_menu.png", pause_menu_items)

    game_over_menu_items = []
    game_over_menu = Menu(game_instance.screen, "./resources/UI/game_over.png", game_over_menu_items)

    credits_items = [
        RollingScreen.RollingScreenItem("Project Director"),
        RollingScreen.RollingScreenItem("Maximilian Fernaldy"),
        RollingScreen.RollingScreenItem(""),
        RollingScreen.RollingScreenItem("Art Director"),
        RollingScreen.RollingScreenItem("Maximilian Fernaldy"),
        RollingScreen.RollingScreenItem(""),
    ]
    credits = RollingScreen(credits_items)

    while True:
        clock.tick(frames_per_second)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_instance.game_state = "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_instance.game_state == "play":
                        game_instance.game_state = "pause"
                    elif game_instance.game_state == "pause":
                        game_instance.game_state = "play"

                if event.key == pygame.K_w:
                    game_instance.current_level.player.up_pressed = True
                if event.key == pygame.K_a:
                    game_instance.current_level.player.left_pressed = True
                if event.key == pygame.K_s:
                    game_instance.current_level.player.down_pressed = True
                if event.key == pygame.K_d:
                    game_instance.current_level.player.right_pressed = True

                if event.key == pygame.K_j:
                    game_instance.current_level.player.lt_atk_pressed = True
                if event.key == pygame.K_k:
                    game_instance.current_level.player.hv_atk_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    game_instance.current_level.player.up_pressed = False
                if event.key == pygame.K_a:
                    game_instance.current_level.player.left_pressed = False
                if event.key == pygame.K_s:
                    game_instance.current_level.player.down_pressed = False
                if event.key == pygame.K_d:
                    game_instance.current_level.player.right_pressed = False

                if event.key == pygame.K_j:
                    game_instance.current_level.player.lt_atk_pressed = False
                if event.key == pygame.K_k:
                    game_instance.current_level.player.hv_atk_pressed = False
        if game_instance.game_state == "quit":
            quit_game()
            break
        
        if game_instance.game_state == "start screen":
            start_menu.update()
        elif game_instance.game_state == "game over":
            game_over_menu.update()
        elif game_instance.game_state == "play":
            game_instance.current_level.update(game_instance.screen)
            if game_instance.current_level.player.health <= 0:
                game_instance.game_state = "game over"
        elif game_instance.game_state == "pause":
            pause_menu.update()
        elif game_instance.game_state == "won":
            if game_instance.current_stage < len(game_instance.level_data):
                game_instance.game_state = "continue screen"
            else:
                credits.update(game_instance.screen)
        elif game_instance.game_state == "continue screen":
            continue_menu.update()

if __name__ == "__main__":
    main()

