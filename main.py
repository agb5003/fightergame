'''
FIGHTER GAME
Maximilian Fernaldy
Spring 2024
Computer Seminar I final project
'''

import sys
import pygame
from entities import Enemy, Player
from game_management import Stage, Map
from ui_elements import HealthBar, Menu

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

STAGES = [
    Level()
]

class Level:
    def __init__(self, player_health, number_of_enemies, enemies_damage):
        # Initialize sprite groups
        self.enemies = pygame.sprite.Group()
        self.protags = pygame.sprite.Group()

        self.player = Player(player_health)
        self.player.rect.left = 50
        self.player.rect.centery = 360

        for i in range(number_of_enemies):
            enemy = Enemy()
            self.enemies.add()

    def __init__(self, stage):
        print("init called")
        self.stage = stage
        
        # Initialize sprite groups
        self.enemies = pygame.sprite.Group()
        self.protags = pygame.sprite.Group()
        
        # Clean up previous level
        self.enemies.empty()
        self.protags.empty()

        self.player = Player()
        self.player.rect.left = 500
        self.player.rect.top = 500
        self.protags.add(self.player)

        # Construct level parameters
        for enemy in STAGES[stage].enemies:
            self.enemies.add(enemy)
        self.player.health = STAGES[stage].player_health

        # Construct UI elements
        self.health_bar = HealthBar(self.player.health)

        # Load new map
        self.map = STAGES[stage].map

        self.game_state = "play"

    def restart(self):
        # Start from the beginning of current level
        self.__init__(self.stage)

    def resume(self):
        self.game_state = "play"

    def update(self, window):
        # Update all entities
        window.screen.fill("black")
        self.map.update(window.screen)
        self.enemies.update(window.screen, self.player)
        self.protags.update(window, self.enemies)

        # Update UI elements
        self.health_bar.update(self.player.health, window.screen)

        pygame.display.update()

class Window:
    def __init__(self, dimensions, window_title):
        self.screen = pygame.display.set_mode((dimensions[0], dimensions[1]))
        pygame.display.set_caption(window_title)
        self.traversable_rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])

def start_level(stage):
    return Level(stage=stage)

def quit_game():
    pygame.quit()
    sys.exit()

game_window = Window((1280, 720), "Fighter Game")

def main():
    clock = pygame.time.Clock()
    frames_per_second = 30

    current_level = 0
    level = start_level(current_level)

    pause_menu_items = [Menu.MenuItems("./resources/UI/restart.png", (640, 360), level.restart),
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
            level.update(game_window)
            if level.player.health <= 0:
                print("game over")
                level.game_state = "game over"
        elif level.game_state == "pause":
            pause_menu.update()

if __name__ == "__main__":
    main()
