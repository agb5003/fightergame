import pygame
from player import Player

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighter Game")

def update(screen, objects):
    screen.fill(pygame.Color("black"))
    for object in objects:
        object.update(screen)
        screen.blit(object.surf, object.rect)
    pygame.display.update()

def draw_pause(screen):
    pause_background = pygame.image.load("resources/UI/pause_menu.png")
    pause_background_rect = pause_background.get_rect()
    pause_background_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    screen.blit(pause_background, pause_background_rect)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    frames_per_second = 60
    objects = []

    player = Player(3, 4)
    player.rect.left = 500
    player.rect.top = 500
    objects.append(player)

    should_quit = False
    pause_menu = False

    while True:
        clock.tick(frames_per_second)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pause_menu == False:
                        pause_menu = True
                    else:
                        pause_menu = False

                if event.key == pygame.K_w:
                    player.up_pressed = True
                if event.key == pygame.K_a:
                    player.left_pressed = True
                if event.key == pygame.K_s:
                    player.down_pressed = True
                if event.key == pygame.K_d:
                    player.right_pressed = True
                
                if event.key == pygame.K_j:
                    player.lt_atk_pressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player.up_pressed = False
                if event.key == pygame.K_a:
                    player.left_pressed = False
                if event.key == pygame.K_s:
                    player.down_pressed = False
                if event.key == pygame.K_d:
                    player.right_pressed = False
                
                if event.key == pygame.K_j:
                    player.lt_atk_pressed = False
        if should_quit:
            break

        if pause_menu == False:
            update(screen, objects)
        else:
            draw_pause(screen)

if __name__ == "__main__":
    main()
