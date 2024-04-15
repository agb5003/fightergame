import pygame

class IdleAnimation:
    def __init__(self, actor, frames):
        self.actor = actor
        self.frame_index = 0

        self.frames = [pygame.transform.scale(frame, (300,200)) for frame in frames]
        self.flipped_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]

        self.period = len(self.frames)
        self.animation_speed = 0.4

    def animate(self):
        frame_to_show = int(self.frame_index * self.animation_speed) % self.period
        if self.actor.facing == "right":
            self.actor.surf = self.frames[frame_to_show]
        else:
            self.actor.surf = self.flipped_frames[frame_to_show]
        self.frame_index += 1

class AttackAnimation:
    def __init__(self, actor, windup_frames, linger_frames, cooldown_frames):
        self.actor = actor
        self.frame_index = 0

        self.windup_frames = [pygame.transform.scale(frame, (300,200)) for frame in windup_frames]
        self.linger_frames = [pygame.transform.scale(frame, (300,200)) for frame in linger_frames]
        self.cooldown_frames = [pygame.transform.scale(frame, (300,200)) for frame in cooldown_frames]

        # Generate flipped frames for when character is facing left
        self.flipped_windup_frames = [pygame.transform.flip(frame, True, False) for frame in self.windup_frames]
        self.flipped_linger_frames = [pygame.transform.flip(frame, True, False) for frame in self.linger_frames]
        self.flipped_cooldown_frames = [pygame.transform.flip(frame, True, False) for frame in self.cooldown_frames]

    def animate(self):
        # Change self.actor.surf to the correct frame
        actor_state = self.actor.state
        if actor_state == "windup":
            if self.actor.facing == "right":
                self.actor.surf = self.windup_frames[self.frame_index]
            else:
                self.actor.surf = self.flipped_windup_frames[self.frame_index]
        elif actor_state == "linger":
            if self.actor.facing == "right":
                self.actor.surf = self.linger_frames[self.frame_index]
            else:
                self.actor.surf = self.flipped_linger_frames[self.frame_index]
        elif actor_state == "cooldown":
            if self.actor.facing == "right":
                self.actor.surf = self.cooldown_frames[self.frame_index]
            else:
                self.actor.surf = self.flipped_cooldown_frames[self.frame_index]

class HitterBox:
    def __init__(self, parent, dimensions, linger):
        self.parent = parent
        self.debugsurf = pygame.Surface(dimensions)
        self.rect = self.debugsurf.get_rect()
        self.linger = linger
        self.time_on_screen = 0

        if self.parent.facing == "right":
            self.rect.midleft = self.parent.rect.center
        else:
            self.rect.midright = self.parent.rect.center

        self.parent.child_objects.append(self)
    def update(self):
        self.time_on_screen += 1

class Attack:
    def __init__(self, attacker, reach, sweep, damage, animation):
        self.attacker = attacker
        self.reach = reach
        self.sweep = sweep
        self.damage = damage
        self.animation = animation

        self.should_start_new_phase = False
    def queue(self):
        # Change attacker state to windup to start windup animation
        self.attacker.state = "windup"
        self.attacker.current_attack = self

    def windup(self):
        if self.should_start_new_phase:
            self.animation.frame_index = 0
            self.animation.animate()
            self.should_start_new_phase = False
        else:
            if self.animation.frame_index < len(self.animation.windup_frames):
                self.animation.animate()
            else:
                # Shift to next phase
                self.attacker.state = "linger"
                self.should_start_new_phase = True
        self.animation.frame_index += 1

    def linger(self, enemies):
        if self.should_start_new_phase:
            self.animation.frame_index = 0
            self.animation.animate()
            self.should_start_new_phase = False
            self.enemy_hit = False

            hitterbox = HitterBox(self.attacker, (self.reach, self.sweep), len(self.animation.linger_frames))
            self.attacker.child_objects.append(hitterbox)

        else:
            # Inflict damage
            for hitterbox in self.attacker.child_objects:
                for enemy in enemies:
                    if (not self.enemy_hit) and hitterbox.rect.colliderect(enemy):
                        self.enemy_hit = True
                        enemy.health -= self.damage
            if self.animation.frame_index < len(self.animation.linger_frames):
                self.animation.animate()
            else:
                # Shift to next phase
                self.attacker.state = "cooldown"
                self.should_start_new_phase = True
        self.animation.frame_index += 1

    def cooldown(self):
        if self.should_start_new_phase:
            self.animation.frame_index = 0
            self.animation.animate()
            self.should_start_new_phase = False
        else:
            if self.animation.frame_index < len(self.animation.cooldown_frames):
                self.animation.animate()
            else:
                # Back to idle animation
                self.attacker.state = "idle"
                self.should_start_new_phase = True
            self.animation.frame_index += 1


class Player:
    def __init__(self, screen, enemies):
        self.screen = screen
        self.facing = "right"
        self.enemies = enemies

        self.surf = pygame.transform.scale(pygame.image.load("./resources/Sprites/Brawler-Girl/Idle/idle1.png").convert_alpha(), (300, 200))
        self.rect = pygame.Rect(90, 100, 300, 200)
        self.state = "idle"
        self.current_attack = None

        self.movement_speed = 6
        self.up_pressed = False
        self.left_pressed = False
        self.down_pressed = False
        self.right_pressed = False

        self.lt_atk_pressed = False
        self.hv_atk_pressed = False

        self.child_objects = []

        # Idle animations
        self.idle_animation = IdleAnimation(self,
                                            frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Idle/idle{i}.png").convert_alpha() for i in range(1, 5)])
        self.walk_animation = IdleAnimation(self,
                                            frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Walk/walk{i}.png").convert_alpha() for i in range(1, 11)])

        # Attack animations
        self.lt_atk_animation = AttackAnimation(self,
                                                windup_frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Jab/jab{i}.png").convert_alpha() for i in [1, 1]],
                                                linger_frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Jab/jab{i}.png").convert_alpha() for i in [2, 3, 2]],
                                                cooldown_frames = [pygame.image.load(f"./resources/Sprites/Brawler-Girl/Jab/jab{i}.png").convert_alpha() for i in [1, 1]]
                                                )
        self.hv_atk_animation = AttackAnimation(self,
                                                windup_frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Kick/kick{i}.png").convert_alpha() for i in [1, 2, 3]],
                                                linger_frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Kick/kick{i}.png").convert_alpha() for i in [4, 5, 4]],
                                                cooldown_frames = [pygame.image.load(f"./resources/Sprites/Brawler-Girl/Kick/kick{i}.png").convert_alpha() for i in [2, 1]]
                                                )
        
        # Attacks
        self.light_attack = Attack(self, 100, 20, 15, self.lt_atk_animation)
        self.heavy_attack = Attack(self, 110, 32, 20, self.hv_atk_animation)
        

    def update(self):
        if self.state in ["idle", "walk"]:
            if self.left_pressed or self.up_pressed or self.down_pressed or self.right_pressed:
                self.state = "walk"
                if self.left_pressed and not self.right_pressed:
                    if self.facing != "left":
                        self.facing = "left"
                    self.rect.centerx += -self.movement_speed
                if self.right_pressed and not self.left_pressed:
                    if self.facing != "right":
                        self.facing = "right"
                    self.rect.centerx += self.movement_speed
                if self.up_pressed and not self.down_pressed:
                    self.rect.centery += -self.movement_speed
                if self.down_pressed and not self.up_pressed:
                    self.rect.centery += self.movement_speed
                self.walk_animation.animate()
            else:
                self.state = "idle"
                self.idle_animation.animate()

            # Handle attack button being pressed
            if self.lt_atk_pressed:
                self.light_attack.queue()
            elif self.hv_atk_pressed:
                self.heavy_attack.queue()

        elif self.state == "windup":
            self.current_attack.windup()
        
        elif self.state == "linger":
            self.current_attack.linger(self.enemies)
        
        elif self.state == "cooldown":
            self.current_attack.cooldown()
        
        
        self.child_objects = [object for object in self.child_objects if object.time_on_screen < object.linger]
        
        self.screen.blit(self.surf, self.rect)
        for object in self.child_objects:
            object.update()
