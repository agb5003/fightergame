import pygame

class Player:
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
    lt_atk_windup = 1
    lt_atk_linger = 3
    lt_atk_cooldown = 5
    hv_atk_windup = 5
    hv_atk_linger = 5
    hv_atk_cooldown = 10

    child_objects = []

    class Animation:
        face_left = False
        def __init__(self, object, frames, images):
            # object = object whose surface we want to animate
            # frames = number of frames in the animation
            # images = path to the images corresponding to frames
            self.object = object
            self.frames = frames
            self.images = [pygame.image.load(image).convert() for image in images]
            self.left_images = [""] * self.frames
            for i in range (self.frames):
                self.images[i] = pygame.transform.scale(self.images[i], (300, 200))
            for i in range (self.frames):
                self.left_images[i] = pygame.transform.flip(self.images[i], True, False)

        def __call__(self):
            # Run the animation loop
            animation_index = self.object.frame_index // self.object.animation_period % self.frames
            if self.object.facing == "left":
                frame_to_show = self.left_images[animation_index]
            else:
                frame_to_show = self.images[animation_index]
            self.object.surf = frame_to_show
            if self.object.current_animation == self.object.lt_atk_animation:
                print(animation_index)

    class ChildObject:
        def __init__(self, surf, rect, linger):
            self.surf = surf
            self.rect = rect
            self.linger = linger
        def update(self):
            self.linger -= 1
    
    class Attack:
        def __init__(self, parent, hitbox_dimensions, windup, linger, cooldown, animation):
            self.hitbox_dimensions = hitbox_dimensions
            self.parent = parent
            self.animation = animation

            self.windup_frames = windup
            self.linger_frames = linger
            self.cooldown_frames = cooldown
        def queue(self):
            self.parent.action_queued = self
            self.parent.windup_frames = self.windup_frames
            self.parent.current_animation = self.animation
        def __call__(self):
            self.surf = pygame.Surface(self.hitbox_dimensions)
            self.surf.fill("red")
            self.rect = self.surf.get_rect()
            if self.parent.facing == "right":
                self.rect.midleft = self.parent.rect.center
            else:
                self.rect.midright = self.parent.rect.center
            self.collider = self.parent.ChildObject(self.surf, self.rect, linger=self.linger_frames)
            self.parent.child_objects.append(self.collider)
        def cooldown(self):
            self.parent.cooldown_frames = self.cooldown_frames
    
    def __init__(self, movement_speed, atk_range):
        # Attributes
        self.atk_range = atk_range
        self.speed = movement_speed

        # Appearance
        self.animation_period = 12
        self.frame_index = 0
        player_animations_folder = "./resources/Sprites/Brawler-Girl/"
        self.idle_animation = self.Animation(self, 4, [player_animations_folder + f"Idle/idle{i}.png" for i in range(1,4+1)])
        self.move_animation = self.Animation(self, 10, [player_animations_folder + f"Walk/walk{i}.png" for i in range(1,10+1)])
        self.lt_atk_animation = self.Animation(self, 9, [
            player_animations_folder + f"Jab/jab{i}.png" for i in [1, 2, 3, 3, 1, 1, 1, 1, 1]
        ])
        self.hv_atk_animation = self.Animation(self, 20, [
            player_animations_folder + f"Kick/kick{i}.png" for i in [1, 2, 3, 3, 3, 4, 4, 5, 5, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        ])
                                               
        self.light_attack = self.Attack(self, (50, 20), self.lt_atk_windup, self.lt_atk_linger, self.lt_atk_cooldown, self.lt_atk_animation)
        self.heavy_attack = self.Attack(self, (150, 30), self.hv_atk_windup, self.hv_atk_linger, self.hv_atk_cooldown, self.hv_atk_animation)
        self.current_animation = self.idle_animation
        self.current_animation()

        self.rect = self.surf.get_rect()
    
    def update(self, screen):
        if self.cooldown_frames == 0:
            # Movement and attack queuing is enabled when not on action cooldown
            if not self.action_queued:
                # Movement
                if self.left_pressed or self.right_pressed or self.up_pressed or self.down_pressed:
                    if self.left_pressed and not self.right_pressed:
                        if self.facing != "left":
                            self.facing = "left"
                        self.rect.centerx += -self.speed
                    if self.right_pressed and not self.left_pressed:
                        if self.facing != "right":
                            self.facing = "right"
                        self.rect.centerx += self.speed
                    if self.up_pressed and not self.down_pressed:
                        self.rect.centery += -self.speed
                    if self.down_pressed and not self.up_pressed:
                        self.rect.centery += self.speed
                    
                    self.current_animation = self.move_animation
                else:
                    self.current_animation = self.idle_animation
            
                # Attack queuing
                if self.lt_atk_pressed:
                    self.frame_index = 0
                    self.light_attack.queue()
                if self.hv_atk_pressed:
                    self.frame_index = 0
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
            if self.current_animation != self.idle_animation:
                self.current_animation = self.idle_animation
            self.cooldown_frames -= 1

        # Run whichever animation is appropriate
        self.frame_index += 1
        self.current_animation()
        
        for child_object in self.child_objects:
            child_object.update()
            screen.blit(child_object.surf, child_object.rect)

        # Cull old hitboxes
        self.child_objects[:] = [child_object for child_object in self.child_objects if child_object.linger > 0]
