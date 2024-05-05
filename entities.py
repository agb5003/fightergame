import math
import pygame

class LinearAnimation:
    last_frame_shown = False
    def __init__(self, actor, frames):
        self.actor = actor
        self.frame_index = 0

        self.rawframes = [pygame.transform.scale(frame, (300,200)) for frame in frames]

        self.frames = [frame.convert_alpha() for frame in self.rawframes]
        self.flipped_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]

        self.period = len(self.frames)
        self.animation_speed = 0.4

    def animate(self):
        if self.last_frame_shown == True:
            self.last_frame_shown = False
        frame_to_show = min(len(self.frames)-1, int(self.frame_index * self.animation_speed))
        if self.actor.facing == "right":
            self.actor.surf = self.frames[frame_to_show]
        else:
            self.actor.surf = self.flipped_frames[frame_to_show]

        self.frame_index += 1

        if len(self.frames) == int(self.frame_index * self.animation_speed):
            self.last_frame_shown = True
            self.frame_index = 0


class LoopingAnimation(LinearAnimation):
    def __init__(self, actor, frames):
        super().__init__(actor, frames)

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

        self.windup_frames = [pygame.transform.scale(frame, (300,200)).convert_alpha() for frame in windup_frames]
        self.linger_frames = [pygame.transform.scale(frame, (300,200)).convert_alpha() for frame in linger_frames]
        self.cooldown_frames = [pygame.transform.scale(frame, (300,200)).convert_alpha() for frame in cooldown_frames]

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
    def __init__(self, parent, dimensions, attachpoint, linger):
        self.parent = parent
        self.debugsurf = pygame.Surface(dimensions)
        self.rect = pygame.Rect((0,0), dimensions)
        self.linger = linger
        self.time_on_screen = 0

        if self.parent.facing == "right":
            self.rect.midleft = attachpoint["right"]
        else:
            self.rect.midright = attachpoint["left"]

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
        self.enemy_hit = False

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

            hitterbox = HitterBox(self.attacker, (self.reach, self.sweep), {"left":(self.attacker.rect.left, self.attacker.rect.centery - 25), "right":(self.attacker.rect.right, self.attacker.rect.centery - 25)}, len(self.animation.linger_frames))
            self.attacker.child_objects.append(hitterbox)

        else:
            # Inflict damage
            for hitterbox in self.attacker.child_objects:
                for enemy in enemies:
                    if (not self.enemy_hit) and hitterbox.rect.colliderect(enemy):
                        self.enemy_hit = True
                        enemy.health -= self.damage
                        enemy.state = "hurt"
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

class Player(pygame.sprite.Sprite):
    def __init__(self, health, initial_position):
        super().__init__()
        self.facing = "right"

        self.surf = pygame.transform.scale(pygame.image.load("./resources/Sprites/Brawler-Girl/Idle/idle1.png").convert_alpha(), (300, 200))
        self.shadow_surf = pygame.transform.scale_by(pygame.image.load("./resources/Sprites/shadow.png").convert_alpha(), 4)
        self.rect = pygame.Rect(initial_position, (58, 150))
        self.debugsurf = pygame.Surface((58, 150))
        self.state = "idle"
        self.current_attack = None

        self.health = health
        self.movement_speed = 6
        self.up_pressed = False
        self.left_pressed = False
        self.down_pressed = False
        self.right_pressed = False

        self.lt_atk_pressed = False
        self.hv_atk_pressed = False

        self.child_objects = []

        # Idle animations
        self.idle_animation = LoopingAnimation(self,
                                            frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Idle/idle{i}.png") for i in range(1, 5)])
        self.walk_animation = LoopingAnimation(self,
                                            frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Walk/walk{i}.png") for i in range(1, 11)])

        # Attack animations
        self.lt_atk_animation = AttackAnimation(self,
                                                windup_frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Jab/jab{i}.png") for i in [1, 2]],
                                                linger_frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Jab/jab{i}.png") for i in [2, 3]],
                                                cooldown_frames = [pygame.image.load(f"./resources/Sprites/Brawler-Girl/Jab/jab{i}.png") for i in [1]]
                                                )
        self.hv_atk_animation = AttackAnimation(self,
                                                windup_frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Kick/kick{i}.png") for i in [1, 2, 3]],
                                                linger_frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Kick/kick{i}.png") for i in [4, 5, 4]],
                                                cooldown_frames = [pygame.image.load(f"./resources/Sprites/Brawler-Girl/Kick/kick{i}.png") for i in [2, 1]]
                                                )
        # Hurt animation
        self.hurt_animation = LinearAnimation(self,
                                            frames=[pygame.image.load(f"./resources/Sprites/Brawler-Girl/Hurt/hurt{i}.png") for i in range(1, 3)])

        # Attacks
        self.light_attack = Attack(self, 80, 20, 15, self.lt_atk_animation)
        self.heavy_attack = Attack(self, 80, 32, 20, self.hv_atk_animation)


    def update(self, enemies, map):
        if self.state in ["idle", "walk"]:
            if self.left_pressed or self.up_pressed or self.down_pressed or self.right_pressed:
                self.state = "walk"
                if self.left_pressed and not self.right_pressed:
                    if self.facing != "left":
                        self.facing = "left"
                    self.rect.centerx += -self.movement_speed
                elif self.right_pressed and not self.left_pressed:
                    if self.facing != "right":
                        self.facing = "right"
                    self.rect.centerx += self.movement_speed
                if self.up_pressed and not self.down_pressed:
                    self.rect.centery += -self.movement_speed
                elif self.down_pressed and not self.up_pressed:
                    self.rect.centery += self.movement_speed

                self.walk_animation.animate()

                if not map.traversable_rect.contains(self.rect):
                    self.rect.clamp_ip(map.traversable_rect)
            else:
                self.state = "idle"
                self.idle_animation.animate()

            # Handle attack button being pressed
            if self.lt_atk_pressed:
                self.light_attack.queue()
            elif self.hv_atk_pressed:
                self.heavy_attack.queue()

        elif self.state == "hurt":
            if self.health <= 0:
                self.kill()
            else:
                self.hurt_animation.animate()
                if self.hurt_animation.last_frame_shown:
                    self.state = "idle"

        elif self.state == "windup":
            self.current_attack.windup()

        elif self.state == "linger":
            self.current_attack.linger(enemies)

        elif self.state == "cooldown":
            self.current_attack.cooldown()

        self.child_objects = [object for object in self.child_objects if object.time_on_screen < object.linger]

        for object in self.child_objects:
            object.update()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, initial_position, damage):
        self.initial_position = initial_position
        self.damage = damage

        super().__init__()
        self.facing = "left"
        self.is_alive = True
        self.max_health = 50
        self.health = self.max_health
        self.child_objects = []

        self.surf = pygame.transform.scale(pygame.image.load("./resources/Sprites/Enemy-Punk/Idle/idle1.png").convert_alpha(), (300, 200))
        self.shadow_surf = pygame.transform.scale_by(pygame.image.load("./resources/Sprites/shadow.png").convert_alpha(), 4)

        # self.debugsurf = pygame.Surface((80, 150))
        # self.rect = self.debugsurf.get_rect()
        # self.rect.center = initial_position
        self.rect = pygame.Rect(initial_position, (80, 150))
        self.state = "idle"
        self.current_attack = None

        self.movement_speed = 2


        # Idle animations
        self.idle_animation = LoopingAnimation(self,
                                            frames=[pygame.image.load(f"./resources/Sprites/Enemy-Punk/Idle/idle{i}.png") for i in range(1, 5)])
        self.walk_animation = LoopingAnimation(self,
                                            frames=[pygame.image.load(f"./resources/Sprites/Enemy-Punk/Walk/walk{i}.png") for i in range(1, 5)])

        # Attack animations
        self.atk_animation = AttackAnimation(self,
                                                windup_frames=[pygame.image.load(f"./resources/Sprites/Enemy-Punk/Punch/punch{i}.png") for i in [1, 2]],
                                                linger_frames=[pygame.image.load(f"./resources/Sprites/Enemy-Punk/Punch/punch{i}.png") for i in [3, 3]],
                                                cooldown_frames = [pygame.image.load(f"./resources/Sprites/Enemy-Punk/Punch/punch{i}.png") for i in [2, 2, 2, 1, 1, 1, 1, 1]]
                                                )

        # Hurt animation
        self.hurt_animation = LinearAnimation(self,
                                            frames=[pygame.image.load(f"./resources/Sprites/Enemy-Punk/Hurt/hurt{i}.png") for i in [1, 2, 2, 1]])

        # KO animation
        self.knockout_animation = LinearAnimation(self,
                                                frames=[pygame.image.load(f"./resources/Sprites/Enemy-Punk/Hurt/hurt{i}.png") for i in range(1,5)])

        # Attacks
        self.attack = Attack(self, 60, 15, damage, self.atk_animation)

    def copy(self):
        # This method is used to copy enemy data to the level when it is started
        # from the beginning.
        return Enemy(self.initial_position, self.damage)

    def update(self, player):
        # Get current distance to player
        x_distance_to_player = self.rect.centerx - player.rect.centerx
        y_distance_to_player = self.rect.centery - player.rect.centery
        distance_to_player = math.sqrt(x_distance_to_player**2 + y_distance_to_player**2)
        abs_x_distance = math.sqrt(x_distance_to_player**2)
        abs_y_distance = math.sqrt(y_distance_to_player**2)

        # Check if player is inside detection zone
        if self.state in ["idle", "walk"]:
            if distance_to_player < 300 and (abs_x_distance > 65 or abs_y_distance > 10):
                if x_distance_to_player < 0:
                    self.facing = "right"
                elif x_distance_to_player > 0:
                    self.facing = "left"
                self.state = "walk"
            else:
                self.state = "idle"

        if self.state == "idle":
            if abs_x_distance <= 65 and abs_y_distance <= 10:
                self.attack.queue()
            else:
                self.idle_animation.animate()
            pass

        elif self.state == "hurt":
            if self.health <= 0:
                if self.knockout_animation.last_frame_shown:
                    pass
                else:
                    self.knockout_animation.animate()
                    # self.kill()
            else:
                self.hurt_animation.animate()
                if self.hurt_animation.last_frame_shown:
                    self.state = "idle"

        elif self.state == "walk":
            if self.facing == "left":
                self.rect.centerx += -self.movement_speed
            else:
                self.rect.centerx += self.movement_speed
            if y_distance_to_player < 0:
                self.rect.centery += self.movement_speed
            else:
                self.rect.centery += -self.movement_speed
            self.walk_animation.animate()

        elif self.state == "windup":
            self.current_attack.windup()

        elif self.state == "linger":
            self.current_attack.linger([player])

        elif self.state == "cooldown":
            self.current_attack.cooldown()

        self.child_objects = [object for object in self.child_objects if object.time_on_screen < object.linger]

        # DEBUGGING ONLY
        # screen.blit(self.debugsurf, self.rect)

        for object in self.child_objects:
            object.update()

        # screen.blit(self.surf, (self.rect.centerx - 150, self.rect.top - 50))
