import pygame

class Player:
    surf = pygame.Surface((50, 120))
    surf.fill("red")
    rect = surf.get_rect()

    facing = "right"
    up_pressed = False
    left_pressed = False
    down_pressed = False
    right_pressed = False

    action_queued = False
    action_on_cooldown = False
    cooldown_frames = 0
    windup_frames = 0

    lt_atk_pressed = False
    hv_atk_pressed = False
    lt_atk_windup = 2
    lt_atk_linger = 5
    lt_atk_cooldown = 6
    hv_atk_windup = 20
    hv_atk_linger = 7
    hv_atk_cooldown = 50

    child_objects = []

    class ChildObject:
        def __init__(self, surf, rect, linger):
            self.surf = surf
            self.rect = rect
            self.linger = linger
        def update(self):
            self.linger -= 1
    
    class Attack:
        def __init__(self, parent, hitbox_dimensions, windup, linger, cooldown):
            self.hitbox_dimensions = hitbox_dimensions
            self.parent = parent

            self.windup_frames = windup
            self.linger_frames = linger
            self.cooldown_frames = cooldown
        def queue(self):
            print(f"queuing {self}")
            self.parent.action_queued = self
            self.parent.windup_frames = self.windup_frames
        def __call__(self):
            print(f"{self}")
            self.surf = pygame.Surface(self.hitbox_dimensions)
            self.surf.fill("pink")
            self.rect = self.surf.get_rect()
            if self.parent.facing == "right":
                self.rect.midleft = self.parent.rect.midright
            else:
                self.rect.midright = self.parent.rect.midleft
            self.collider = self.parent.ChildObject(self.surf, self.rect, linger=self.linger_frames)
            self.parent.child_objects.append(self.collider)
        def cooldown(self):
            print(f"cooldown init by {self}")
            self.parent.action_on_cooldown = True
            self.parent.cooldown_frames = self.cooldown_frames
    
    def __init__(self, movement_speed, atk_range):
        self.atk_range = atk_range
        self.speed = movement_speed
        self.light_attack = self.Attack(self, (50, 20), 3, 3, 10)
        self.heavy_attack = self.Attack(self, (150, 30), 20, 10, 20)
    
    def update(self, screen):
        if self.cooldown_frames <= 0:
            # Remove cooldown status when cooldown is over
            self.action_on_cooldown = False
        if not self.action_on_cooldown:
            # Movement and attack queuing is enabled when not on action cooldown

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

            # Attack queuing
            if not self.action_queued:
                if self.lt_atk_pressed:
                    self.light_attack.queue()

                if self.hv_atk_pressed:
                    self.heavy_attack.queue()
            else:
                # If an action is in queue, decrease windup by 1
                self.windup_frames -= 1
                if self.windup_frames == 0:
                    # Call the action in the queue when the windup is done
                    self.action_queued()
                    # Initiate cooldown
                    self.action_queued.cooldown()
                    # Clear action queue
                    self.action_queued = None
        else:
            self.cooldown_frames -= 1
        
        for child_object in self.child_objects:
            child_object.update()
            screen.blit(child_object.surf, child_object.rect)

        # Cull old hitboxes
        self.child_objects[:] = [child_object for child_object in self.child_objects if child_object.linger > 0]