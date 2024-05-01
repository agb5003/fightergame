import json
import pygame
from entities import Enemy, Player
from ui_elements import HealthBar

LEVEL_DATA = {
    "1": {
        "map": "./resources/cyberpunk-street-files/Version 1/PNG/cyberpunk-street.png",
        "scale": 3.75,
        "traversable_area": [0, 450, 2280, 270],
        "player_health": 100,
        "player_initial_position": [40, 400],
        "enemy_positions": [
            [40,450],
            [800, 350],
        ],
        "enemy_damage": 5
    },
    "2": {
        "map": "./resources/Miami-synth-files/Layers/highway.png",
        "scale": 3,
        "traversable_area": [0, 400, 2688, 320],
        "player_health": 100,
        "player_initial_position": [40, 400],
        "enemy_positions": [
            [400, 550],
            [1200, 650],
            [1000, 490]
        ],
        "enemy_damage": 10
    }
}

class GameInstance:
    def __init__(self, screen_dimensions, window_title):
        self.screen = pygame.display.set_mode(screen_dimensions)
        pygame.display.set_caption(window_title)
        
        with open("leveldata.json") as level_file:
            self.level_data = json.load(level_file)

        self.game_state = "start screen"
        self.current_stage = 0
        self.current_level = Level(self)
    def start_next_stage(self):
        self.current_stage += 1
        self.current_level = Level(self)
        self.current_level.start_from_beginning()

class Level:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        stage = self.game_instance.current_stage

        current_stage_data = self.game_instance.level_data[str(stage)]

        self.protags = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.camera_group = CameraGroup()

        self.player_max_health = current_stage_data["player_health"]
        self.player_initial_position = current_stage_data["player_initial_position"]
        self.enemies_data = [Enemy(pos, current_stage_data["enemy_damage"]) for pos in current_stage_data["enemy_positions"]]
        self.player = Player(0, (0,0))

        self.map = Map(current_stage_data["map"], current_stage_data["scale"], pygame.Rect(*current_stage_data["traversable_area"]))

    def start_from_beginning(self):
        # Reset entities and sprite groups
        self.protags.empty()
        self.enemies.empty()
        self.player = Player(self.player_max_health, self.player_initial_position)
        self.player.rect.topleft = self.player_initial_position
        self.protags.add(self.player)
        for enemy in self.enemies:
            enemy.health = enemy.max_health
            print(enemy.max_health)
        
        # Construct UI elements
        self.health_bar = HealthBar(self.player_max_health)

        # Start gameplay
        self.game_instance.game_state = "play"

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
        if [enemy for enemy in self.enemies if enemy.health > 0] == []:
            self.game_instance.game_state = "won"

        pygame.display.update()

class Map:
    def __init__(self, background_image, scale, traversable_rect):
        self.background = pygame.image.load(background_image).convert_alpha()
        self.background = pygame.transform.scale_by(self.background, scale)
        self.background_rect = self.background.get_rect()
        self.background_rect.topleft = (0, 0)
        self.traversable_rect = traversable_rect
    def update(self):
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

