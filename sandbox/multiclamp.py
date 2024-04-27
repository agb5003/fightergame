import pygame

# Define the irregular area as a list of rectangles
irregular_area = [
    pygame.Rect(100, 100, 200, 50),
    pygame.Rect(200, 150, 100, 200),
    pygame.Rect(100, 250, 200, 100)
]

last_containing_rect = None

# Function to check if a rectangle is contained within the irregular area
def is_contained(rect):
    global last_containing_rect
    for area in irregular_area:
        if area.contains(rect):
            last_containing_rect = area
            return True
    return False

# Example usage
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

player_rect = pygame.Rect(50, 50, 30, 30)

running = True
while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_UP]:
        player_rect.y -= 5
    if keys[pygame.K_DOWN]:
        player_rect.y += 5

    # Ensure the player rectangle stays within the irregular area
    if not is_contained(player_rect):
        if not last_containing_rect: # If last_containing_rect is None (e.g. when first started)
            player_rect.clamp_ip(irregular_area[0])
        else:
            player_rect.clamp_ip(last_containing_rect)

    pygame.draw.rect(screen, (0, 0, 255), player_rect)
    for area in irregular_area:
        pygame.draw.rect(screen, (255, 0, 0), area, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
