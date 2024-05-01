'''
FIGHTER GAME
Maximilian Fernaldy
Spring 2024
Computer Seminar I final project
'''

import sys
import pygame
from entities import Enemy
from game_manager import Map, Level
from ui_elements import Menu, RollingScreen

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def quit_game():
    pygame.quit()
    sys.exit()

class Window:
    def __init__(self, dimensions, window_title):
        self.screen = pygame.display.set_mode((dimensions[0], dimensions[1]))
        pygame.display.set_caption(window_title)

game_window = Window((1280, 720), "Fighter Game")

def main():
    LEVELS = [
        Level(Map("./resources/cyberpunk-street-files/Version 1/PNG/cyberpunk-street.png", 3.75, pygame.Rect(0, 450, 2280, SCREEN_HEIGHT-450)),
        player_health=100, player_initial_position=(40, 400), enemies=[
            Enemy((40, 450), 5),
            Enemy((800, 350), 5)
            # Enemy((1000, 390), 5),
            # Enemy((200, 480), 5),
            # Enemy((340, 350), 5)
        ]),
        Level(Map("./resources/cyberpunk-street-files/Version 1/PNG/cyberpunk-street.png", 3.75, pygame.Rect(0, 450, 2280, SCREEN_HEIGHT-450)),
        player_health=100, player_initial_position=(40, 400), enemies=[
            Enemy((40, 450), 5),
            Enemy((800, 350), 5),
            Enemy((1000, 390), 5),
            # Enemy((200, 480), 5),
            # Enemy((340, 350), 5)
        ]),
    ]

    clock = pygame.time.Clock()
    frames_per_second = 60

    stage = 0
    level = LEVELS[stage]

    start_menu_items = [Menu.MenuItemTextOnly("New Game", (640, 360), level.start_from_beginning)]
    start_menu = Menu(game_window.screen, "./resources/UI/pause_menu.png", start_menu_items)

    continue_menu_items = [Menu.MenuItemTextOnly("Next level", (640, 360), level.)]

    pause_menu_items = [Menu.MenuItem("./resources/UI/restart.png", (640, 360), level.start_from_beginning),
                        Menu.MenuItem("./resources/UI/quit.png", (640, 500), quit_game)]
    pause_menu = Menu(game_window.screen, "./resources/UI/pause_menu.png", pause_menu_items)

    game_over_menu_items = []
    game_over_menu = Menu(game_window.screen, "./resources/UI/game_over.png", game_over_menu_items)

    credits_items = [
        RollingScreen.RollingScreenItem("Project Director"),
        RollingScreen.RollingScreenItem("Maximilian Fernaldy"),
        RollingScreen.RollingScreenItem(""),
        RollingScreen.RollingScreenItem("Art Director"),
        RollingScreen.RollingScreenItem("Maximilian Fernaldy"),
        RollingScreen.RollingScreenItem(""),
        RollingScreen.RollingScreenItem("Ngewemaster"),
        RollingScreen.RollingScreenItem("Maximilian Fernaldy"),
    ]
    credits = RollingScreen(credits_items)

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
        
        if level.game_state == "start screen":
            start_menu.update()
        elif level.game_state == "game over":
            game_over_menu.update()
        elif level.game_state == "play":
            level.update(game_window.screen)
            if level.player.health <= 0:
                print("game over")
                level.game_state = "game over"
        elif level.game_state == "pause":
            pause_menu.update()
        elif level.game_state == "won":
            stage += 1
            if stage < len(LEVELS):
                level = LEVELS[stage]
                level.start_from_beginning()
            else:
                credits.update(game_window.screen)

if __name__ == "__main__":
    main()

