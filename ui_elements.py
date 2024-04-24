import pygame

class Menu:
    class MenuItems:
        def __init__(self, image, position, function=None):
            self.image = pygame.image.load(image).convert_alpha()
            self.function = function
            self.position = position
    def __init__(self, screen, background_image, items):
        self.screen = screen
        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        self.background = pygame.image.load(background_image).convert_alpha()
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (self.SCREEN_WIDTH/2, self.SCREEN_HEIGHT/2)

        # load images for menu items
        self.items = items
        for item in self.items:
            item.rect = item.image.get_rect()
            item.rect.center = item.position

    def update(self):
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        for item in self.items:
            if item.rect.collidepoint(mouse_pos):
                item.image.set_alpha(100)
                if mouse_state[0]:
                    item.function()
            else:
                item.image.set_alpha(255)


        self.screen.blit(self.background, self.background_rect)
        for item in self.items:
            self.screen.blit(item.image, item.rect)
        
        pygame.display.update()

class HealthBar:
    def __init__(self, max_value):
        self.max_value = max_value
        self.surf = pygame.Surface((200, 30))
        self.position = (40, 40)
        self.surf.fill("green")
        self.text = f"Health: {self.max_value}"

        self.font = pygame.font.Font("./resources/UI/pixeltype.ttf", size=64)

    def update(self, new_value, screen):
        self.value = new_value
        self.surf = pygame.Surface((new_value/self.max_value * 200, 30))
        self.surf.fill("green")

        self.text = f"Health: {self.value}"

        self.textsurf = self.font.render(self.text, False, "white")
        self.textpos = (20,20)

        screen.blit(self.surf, self.position)
        screen.blit(self.textsurf, self.textpos)
