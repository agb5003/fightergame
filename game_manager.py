import pygame
from entities import Player
from ui_elements import HealthBar

class Level:
    def __init__(self, map, player_health, player_initial_position, enemies):
        self.player_max_health = player_health
        self.player_initial_position = player_initial_position
        self.enemies_data = enemies
        self.player = Player(0, (0,0))

        self.game_state = "start screen"

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
        self.camera_group = CameraGroup()
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

        self.camera_group.custom_draw(self.player, self.map)

        # Update UI elements
        self.health_bar.update(self.player.health, screen)

        # Check win condition
        if not self.enemies:
            self.game_state = "won"

        pygame.display.update()

class Map:
    def __init__(self, background_image, scale, traversable_rect):
        self.background = pygame.image.load(background_image).convert_alpha()
        self.background = pygame.transform.scale_by(self.background, scale)
        self.background_rect = self.background.get_rect()
        self.background_rect.topleft = (0, 0)
        self.traversable_rect = traversable_rect
        # self.traversable_rect_offset = pygame.math.Vector2(0,traversable_rect.top)
    def update(self):
        # screen = pygame.display.get_surface()
        # self.traversable_rect.topleft = self.background_rect.topleft + self.traversable_rect_offset
        pass

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

        # Camera box
        self.camera_boundaries = {"left": 150, "right": 150}
        self.camera_rect = pygame.Rect(self.camera_boundaries["left"], 0, self.screen.get_width() - (self.camera_boundaries["left"] + self.camera_boundaries["right"]), self.screen.get_height())

        self.offset = pygame.math.Vector2(self.camera_boundaries["left"],0)

    def move_camera(self, target, map):
        if target.rect.left < self.camera_rect.left and target.rect.left > self.camera_boundaries["left"]:
            self.camera_rect.left = target.rect.left
        elif target.rect.right > self.camera_rect.right and target.rect.right < map.background.get_width() - self.camera_boundaries["right"]:
            self.camera_rect.right = target.rect.right

        self.offset.x = self.camera_rect.left - self.camera_boundaries["left"]

    def custom_draw(self, player, map):

        self.move_camera(player, map)

        # Draw map
        map_offset = map.background_rect.topleft - self.offset

        # Compensate for transparent space in entity PNG files
        entity_offset = pygame.math.Vector2(120, 50)

        self.screen.blit(map.background, map_offset)

        # Draw entities
        for entity in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = entity.rect.topleft - self.offset - entity_offset
            self.screen.blit(entity.surf, offset_position)

