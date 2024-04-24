import pygame

class Map:
    def __init__(self, background_image):
        self.background = pygame.image.load(background_image).convert_alpha()
        self.background = pygame.transform.scale_by(self.background, 3)
        self.background_rect = self.background.get_rect()
        self.background_rect.topleft = (0, 0)
        self.traversable_zone = pygame.Rect(0, 100, 1200*3, 140*3)
    def update(self, screen):
        screen.blit(self.background, self.background_rect)