import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Ball")

# Load the image with transparency
image = pygame.image.load("./resources/Sprites/Brawler-Girl/Idle/idle1.png").convert_alpha()
ball = pygame.draw.circle(screen, "green", (400,300), 6)

ball_mask = pygame.mask.from_surface(ball)

# Get the rect of the image
image_rect = image.get_rect()

# Create a mask for the image
image_mask = pygame.mask.from_surface(image)

# Ball properties
ball_radius = 20
ball_color = (255, 0, 0)
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_speed_x = 5
ball_speed_y = 5

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce off the walls
    if ball_x - ball_radius < 0 or ball_x + ball_radius > screen_width:
        ball_speed_x *= -1
    if ball_y - ball_radius < 0 or ball_y + ball_radius > screen_height:
        ball_speed_y *= -1

    # Check for collision with the image
    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
    overlap = image_mask.overlap_area(ball_mask, (ball_rect.x - image_rect.x, ball_rect.y - image_rect.y))
    if overlap > 0:
        # If collision detected, reverse the ball's direction
        ball_speed_x *= -1
        ball_speed_y *= -1

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the image
    screen.blit(image, image_rect)

    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
