'''
FIGHTER GAME
Maximilian Fernaldy
Spring 2024
Computer Seminar I final project
'''

import sys
import pygame
from game_manager import GameInstance
from ui_elements import Menu, RollingScreen

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def quit_game():
    pygame.quit()
    sys.exit()

def main():
    def setup():
        game_instance = GameInstance((1280, 720), "Sendai 11PM")

        start_menu_items = [Menu.MenuItemTextOnly("Start Game", (640, 360), game_instance.current_level.start_from_beginning),
                            Menu.MenuItemTextOnly("Quit", (640, 500), quit_game)]
        start_menu = Menu(game_instance.screen, "./resources/UI/start_screen.png", start_menu_items)

        continue_menu_items = [Menu.MenuItemTextOnly("Next level", (640, 360), game_instance.goto_next_stage)]
        continue_menu = Menu(game_instance.screen, "./resources/UI/level_cleared.png", continue_menu_items)

        pause_menu_items = [Menu.MenuItemTextOnly("Restart level", (640, 360), game_instance.restart_stage),
                            Menu.MenuItemTextOnly("Quit to desktop", (640, 500), quit_game)]
        pause_menu = Menu(game_instance.screen, "./resources/UI/pause_menu.png", pause_menu_items)

        game_over_menu_items = [Menu.MenuItemTextOnly("Restart level", (640, 360), game_instance.restart_stage),
                                Menu.MenuItemTextOnly("Quit to desktop", (640, 500), quit_game)]
        game_over_menu = Menu(game_instance.screen, "./resources/UI/game_over.png", game_over_menu_items)

        credits_items = [
            RollingScreen.RollingScreenItem("Project Director"),
            RollingScreen.RollingScreenItem("Maximilian Fernaldy"),
            RollingScreen.RollingScreenItem(""),
            RollingScreen.RollingScreenItem("Technical Director"),
            RollingScreen.RollingScreenItem("Maximilian Fernaldy"),
            RollingScreen.RollingScreenItem(""),
            RollingScreen.RollingScreenItem("Map and character assets by"),
            RollingScreen.RollingScreenItem("Ansimuz on itch.io"),
            RollingScreen.RollingScreenItem("(https://ansimuz.itch.io)"),
            RollingScreen.RollingScreenItem(""),
            RollingScreen.RollingScreenItem("Thank you for playing Sendai 11PM!")
        ]
        credits = RollingScreen(credits_items)

        clock = pygame.time.Clock()
        frames_per_second = 30

        return game_instance, start_menu, continue_menu, pause_menu, game_over_menu, credits, clock, frames_per_second

    game_instance, start_menu, continue_menu, pause_menu, game_over_menu, credits, clock, frames_per_second = setup()
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
        elif game_instance.game_state == "pause":
            pause_menu.update()
        elif game_instance.game_state == "won":
            if game_instance.current_stage < len(game_instance.level_data):
                # Display menu to continue to next level
                game_instance.game_state = "continue screen"
            else:
                credits.update(game_instance)
                if credits.last_item_centery < 150:
                    # When last item has gone on top of y-150
                    # Create a new game instance and go back to start screen
                    game_instance, start_menu, continue_menu, pause_menu, game_over_menu, credits, clock, frames_per_second = setup()
        elif game_instance.game_state == "continue screen":
            continue_menu.update()

if __name__ == "__main__":
    main()

