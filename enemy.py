import pygame

class Enemy:
    def __init__(self, screen):
        self.dimensions = (200, 100)
        self.surf = pygame.Surface(self.dimensions)
        self.surf.fill("red")
        self.rect = self.surf.get_rect()
        self.initpos = (200, 300)
        self.rect.center = self.initpos
        self.health = 100
        self.is_alive = True

        self.screen = screen
        
    def update(self):
        print(f"health is now {self.health}")
        self.screen.blit(self.surf, self.rect)
        if self.health <= 0:
            self.is_alive = False