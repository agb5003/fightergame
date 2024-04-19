'''
FIGHTER GAME
Maximilian Fernaldy
Spring 2024
Computer Seminar I final project
'''

import sys
import pygame
from entities import Enemy, Map
from entities import Player
from ui_elements import Menu

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Level:
    def __init__(self, map, enemies):
        self.objects = []
        self.enemies = []

        player = Player(game_window, enemies=enemies)
        player.rect.left = 500
        player.rect.top = 500
        self.objects.append(player)
        
        enemy = Enemy(game_window, player)
        enemies.append(enemy)

        self.map = map
        self.player = player
        self.enemies = enemies
        self.game_state = None
    def begin(self, stage):
        print("beginning level")
        
        self.game_state = "play"
    def restart(self):
        # Start from the beginning of current level
        self.game_state = "play"
    def resume(self):
        self.game_state = "play"

class Window:
    def __init__(self, dimensions, window_title):
        self.screen = pygame.display.set_mode((dimensions[0], dimensions[1]))
        pygame.display.set_caption(window_title)
        self.traversable_rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])

def update(window, objects, enemies, map):
    window.screen.fill("black")
    map.update(window.screen)
    for enemy in enemies:
        enemy.update()
    for object in objects:
        object.update()
    enemies[:] = [enemy for enemy in enemies if enemy.is_alive]
    pygame.display.update()

def quit_game():
    pygame.quit()
    sys.exit()

def main():
    game_window = Window((1280, 720), "Fighter Game")
    clock = pygame.time.Clock()
    frames_per_second = 60
    game_map = Map("./resources/preview_stage.png")

    level = Level(game_map, 1)

    pause_menu_items = [Menu.MenuItems("./resources/UI/restart.png", (640, 360),level.restart),
                        Menu.MenuItems("./resources/UI/quit.png", (640, 500), quit_game)]
    pause_menu = Menu(game_window.screen, "./resources/UI/pause_menu.png", pause_menu_items)

    game_over_menu_items = []
    game_over_menu = Menu(game_window.screen, "./resources/UI/game_over.png", game_over_menu_items)

    level.game_state = "play"

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
            update(game_window, level.objects, level.enemies, game_map)
            if level.player.health <= 0:
                print("game over")
                level.game_state = "game over"
        elif level.game_state == "pause":
            pause_menu.update()

if __name__ == "__main__":
    main()
