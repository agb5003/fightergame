import game_manager
import pygame

LEVELS = [
    game_manager.Level(player_health=100, enemies=[
        Enemy(initial_position=(200, 400), damage=5)
        Enemy(initial_position=(300, 500), damage=5)
        Enemy(initial_position=(800, 350), damage=5)
    ]),
    game_management.Level(player_health=100, enemies=[
        Enemy(initial_position=(200, 400), damage=5)
        Enemy(initial_position=(300, 500), damage=5)
        Enemy(initial_position=(800, 350), damage=5)
    ]),
    game_management.Level(player_health=100, enemies=[
        Enemy(initial_position=(200, 400), damage=5)
        Enemy(initial_position=(300, 500), damage=5)
        Enemy(initial_position=(800, 350), damage=5)
    ]),
]
