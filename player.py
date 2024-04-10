import pygame

class Player():
    surf = pygame.Surface((50, 120))
    surf.fill("red")
    rect = surf.get_rect()

    facing = "right"
    up_pressed = False
    left_pressed = False
    down_pressed = False
    right_pressed = False

    action_on_cooldown = False
    cooldown_frames = 0
    frames_to_wait = 0

    lt_atk_pressed = False
    hv_atk_pressed = False
    lt_atk_linger = 5
    lt_atk_cooldown = 6
    hv_atk_cooldown = 120

    child_objects = []

    class ChildObject():
        def __init__(self, surf, rect, linger):
            self.surf = surf
            self.rect = rect
            self.linger = linger
        def update(self, screen):
            print(f"linger is now {self.linger}")
            self.linger -= 1
    
    def __init__(self, movement_speed, atk_range):
        self.atk_range = atk_range
        self.speed = movement_speed

    def start_cooldown(self):
        self.cooldown_frames = 0

    def light_attack(self):
        self.frames_to_wait = self.lt_atk_cooldown
        lt_atk_surf = pygame.Surface((self.atk_range*10, 10))
        lt_atk_surf.fill("pink")
        lt_atk_area = lt_atk_surf.get_rect()
        lt_atk_area.midleft = (self.rect.midright)
        lt_atk_collider = self.ChildObject(lt_atk_surf, lt_atk_area, linger=4)
        self.child_objects.append(lt_atk_collider)
    
    def update(self, screen):
        # Movement
        if self.left_pressed and not self.right_pressed:
            self.facing = "left"
            self.rect.centerx += -self.speed
        if self.right_pressed and not self.left_pressed:
            self.facing = "right"
            self.rect.centerx += self.speed
        if self.up_pressed and not self.down_pressed:
            self.rect.centery += -self.speed
        if self.down_pressed and not self.up_pressed:
            self.rect.centery += self.speed
        
        # Confine to map

        if self.cooldown_frames > self.frames_to_wait:
            self.action_on_cooldown = False
        if not self.action_on_cooldown:
            if self.lt_atk_pressed:
                self.light_attack()
                self.action_on_cooldown = True
                self.start_cooldown()
        else:
            self.cooldown_frames += 1
        
        for child_object in self.child_objects:
            child_object.update(screen)
            screen.blit(child_object.surf, child_object.rect)

        self.child_objects[:] = [child_object for child_object in self.child_objects if child_object.linger > 0]