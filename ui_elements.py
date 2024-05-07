import pygame

class Menu:
    class MenuItem:
        def __init__(self, text, position, function=None, function_parameters=None):
            self.text = text
            self.font = pygame.font.Font("./resources/UI/pixeltype.ttf", 64)
            self.image = self.font.render(self.text, False, "white")
            self.function = function
            self.function_parameters = function_parameters
            self.position = position
            self.pressed = False

    def __init__(self, background_image, items):
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.background = pygame.image.load(background_image).convert_alpha()
        self.background_rect = self.background.get_rect()
        self.background_rect.center = (self.screen_width/2, self.screen_height/2)

        # load images for menu items
        self.items = items
        for item in self.items:
            item.rect = item.image.get_rect()
            item.rect.center = item.position

    def update(self):
        mouse_state = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        self.screen.blit(self.background, self.background_rect)

        for item in self.items:
            displaypos = item.rect.topleft
            if item.rect.collidepoint(mouse_pos):
                item.image.set_alpha(100)
                displaypos = item.rect.topleft + pygame.math.Vector2(-5, 5)
                if mouse_state[0]:
                    item.pressed = True
                elif (not mouse_state[0]) and item.pressed:
                    if item.function_parameters:
                        item.function(*item.function_parameters)
                    else:
                        item.function()
                    item.pressed = False
            else:
                item.pressed = False
                item.image.set_alpha(255)
            self.screen.blit(item.image, displaypos)
            
        
        pygame.display.update()

class HealthBar:
    def __init__(self, max_value):
        self.max_value = max_value
        self.max_width = 300
        self.height = 40
        self.position = (20, 20)

        self.font = pygame.font.Font("./resources/UI/pixeltype.ttf", size=56)

    def update(self, new_value):
        self.value = max(new_value, 0)
        self.surf = pygame.Surface((self.value/self.max_value * self.max_width, self.height))
        self.surf.fill("green")

        self.text = f"Health: {self.value}"

        color = "white" if self.value > 20 else "red"
        self.textsurf = self.font.render(self.text, False, color)
        self.textpos = (26, 26)

class RollingScreen:
    class RollingScreenItem:
        def __init__(self, text):
            font = pygame.font.Font("./resources/UI/pixeltype.ttf", 56)
            self.surf = font.render(text, False, "white")
            self.rect = self.surf.get_rect()
    def __init__(self, items):
        self.halfw = pygame.display.get_surface().get_width()//2
        height = pygame.display.get_surface().get_height()
        self.topmost_y_position = height
        self.items = items
        self.items_opacity = 255
        self.last_item_centery = 0
    def update(self, game_instance):
        game_instance.screen.fill("black")

        offset = 0
        half_screen_height = game_instance.screen.get_height()//2
        if self.last_item_centery < half_screen_height:
            if self.items_opacity - 10 > 0:
                self.items_opacity -= 4
            else:
                self.items_opacity = 0

        for item in self.items:
            item.rect.centerx = self.halfw
            item.rect.centery = self.topmost_y_position + offset
            offset += 50
            self.last_item_centery = item.rect.centery

            item.surf.set_alpha(self.items_opacity)

            game_instance.screen.blit(item.surf, item.rect)
        
        self.topmost_y_position -= 2
        pygame.display.update()

