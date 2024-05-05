import json
import pygame
from entities import Enemy, Player
from ui_elements import HealthBar

class GameInstance:
    def __init__(self, screen_dimensions, window_title):
        self.screen = pygame.display.set_mode(screen_dimensions)
        pygame.display.set_caption(window_title)
        
        with open("leveldata.json") as level_file:
            self.level_data = json.load(level_file)

        self.game_state = "start screen"
        self.current_stage = 1
        self.current_level = Level(self)
    def goto_next_stage(self):
        self.current_stage += 1
        self.current_level = Level(self)
        self.current_level.start_from_beginning()
    def restart_stage(self):
        self.current_level = Level(self)
        self.current_level.start_from_beginning()

class Level:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        stage = self.game_instance.current_stage

        current_stage_data = self.game_instance.level_data[str(stage)]

        self.enemies = []
        self.camera_group = CameraGroup()

        self.player_max_health = current_stage_data["player_health"]
        self.player_initial_position = current_stage_data["player_initial_position"]
        self.enemies_data = [Enemy(pos, current_stage_data["enemy_damage"]) for pos in current_stage_data["enemy_positions"]]
        self.player = Player(0, (0,0))

        self.map = Map(current_stage_data["map"], current_stage_data["scale"], pygame.Rect(*current_stage_data["traversable_area"]))

    def start_from_beginning(self):
        # Reset entities and sprite groups
        self.camera_group.empty()
        self.enemies = []
        self.player = Player(self.player_max_health, self.player_initial_position)
        self.player.rect.topleft = self.player_initial_position
        self.camera_group.add(self.player)

        for enemy in self.enemies_data:
            enemy_copy = enemy.copy()
            self.enemies.append(enemy_copy)
            self.camera_group.add(enemy_copy)
        
        # Construct UI elements
        self.health_bar = HealthBar(self.player_max_health)

        # Start gameplay
        self.game_instance.game_state = "play"

    def resume(self):
        self.game_state = "play"

    def update(self, screen):
        # Update all entities
        screen.fill("black")
        for enemy in self.enemies:
            enemy.update(self.player)
        self.player.update(self.enemies, self.map)

        # Draw map and entities
        self.camera_group.custom_draw(self.player, self.map)

        # Update UI elements
        self.health_bar.update(self.player.health, screen)

        # Check win condition
        alive_enemies = [enemy for enemy in self.enemies if enemy.health > 0]
        knocked_out_enemies = [enemy for enemy in self.enemies if enemy.knockout_animation.last_frame_shown]
        if len(knocked_out_enemies) == len(self.enemies_data):
            self.game_instance.game_state = "won"
        
        # Check player health
        if self.player.health <= 0:
            self.game_instance.game_state = "game over"

        pygame.display.update()

class Map:
    def __init__(self, background_image, scale, traversable_rect):
        self.background = pygame.image.load(background_image).convert_alpha()
        self.background = pygame.transform.scale_by(self.background, scale)
        self.background_rect = self.background.get_rect()
        self.background_rect.topleft = (0, 0)
        self.traversable_rect = traversable_rect

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

        # Camera box
        self.camera_boundaries = {"left": 200, "right": 200}
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

        # Move map relative to box camera
        map_offset = map.background_rect.topleft - self.offset

        # Compensate for transparent space in entity PNG files
        entity_offset = pygame.math.Vector2(120, 50)
        shadow_offset = pygame.math.Vector2(105, 175)

        self.screen.blit(map.background, map_offset)

        # Draw entities
        for entity in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = entity.rect.topleft - self.offset - entity_offset
            self.screen.blit(entity.shadow_surf, offset_position + shadow_offset)
            self.screen.blit(entity.surf, offset_position)

