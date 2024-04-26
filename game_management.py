import pygame
from entities import Player
from ui_elements import HealthBar
from copy import deepcopy

class Level:
    def __init__(self, map, player_health, player_initial_position, enemies):
        self.player_max_health = player_health
        self.player_initial_position = player_initial_position
        self.enemies_data = enemies

        self.map = map

        self.protags = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

    def start_from_beginning(self):
        # Reset entities and sprite groups
        self.player = Player(self.player_max_health, self.player_initial_position)
        self.protags.empty()
        self.enemies.empty()
        self.protags.add(self.player)
        for enemy in self.enemies_data:
            self.enemies.add(enemy.copy())

        print(self.enemies_data)

        # Construct UI elements
        self.health_bar = HealthBar(self.player_max_health)

        # Start gameplay
        self.game_state = "play"

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

class Map:
    def __init__(self, background_image):
        self.background = pygame.image.load(background_image).convert_alpha()
        self.background = pygame.transform.scale_by(self.background, 3)
        self.background_rect = self.background.get_rect()
        self.background_rect.topleft = (0, 0)
        self.traversable_zone = pygame.Rect(0, 100, 1200*3, 140*3)
    def update(self, screen):
        screen.blit(self.background, self.background_rect)
