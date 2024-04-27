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
        self.camera_group = CameraGroup(self.map)
        self.camera_group.add(self.protags, self.enemies)

        # Construct UI elements
        self.health_bar = HealthBar(self.player_max_health)

        # Start gameplay
        self.game_state = "play"

    def resume(self):
        self.game_state = "play"

    def update(self, screen):
        # Update all entities
        screen.fill("black")
        self.enemies.update(self.player)
        self.protags.update(self.enemies, self.map)

        self.map.update()

        self.camera_group.custom_draw(self.player)

        # Update UI elements
        self.health_bar.update(self.player.health, screen)

        pygame.display.update()

class Map:
    def __init__(self, background_image, scale, traversable_rect):
        self.background = pygame.image.load(background_image).convert_alpha()
        self.background = pygame.transform.scale_by(self.background, scale)
        self.background_rect = self.background.get_rect()
        self.background_rect.topleft = (0, 0)
        self.traversable_rect = traversable_rect
        self.traversable_rect_offset = pygame.math.Vector2(0,traversable_rect.top)
    def update(self):
        screen = pygame.display.get_surface()
        # self.traversable_rect.topleft = self.background_rect.topleft + self.traversable_rect_offset
        pass

class CameraGroup(pygame.sprite.Group):
    def __init__(self, map):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.map = map

        # Map background
        self.map_background = map.background
        self.map_rect = map.background_rect

        # player_offset is the offset needed to position the player correctly,
        # as a result of the empty space in the PNG files of the player surface.
        self.player_offset = pygame.math.Vector2(120, 50)
        # This offset is added only to the map_offset to show the map offset down
        # and to the right, with the lengths roughly equaling the distance from the top
        # left pixel of the PNG file to the top left pixel of the player rectangle.

    def center_target_camera(self, target):

        self.offset.x = target.rect.centerx - self.screen.get_width()//2
        self.offset.y = target.rect.centery - self.screen.get_height()//2

    def custom_draw(self, player):

        self.center_target_camera(player)

        # Draw map
        map_offset = self.map_rect.topleft - self.offset + self.player_offset

        pygame.draw.rect(self.screen, "green", self.map.background_rect)
        pygame.draw.rect(self.screen, "red", self.map.traversable_rect)

        self.screen.blit(self.map_background, map_offset)

        # Draw entities
        for entity in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = entity.rect.topleft - self.offset
            self.screen.blit(entity.surf, offset_position)