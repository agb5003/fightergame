import pygame

pygame.init()

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Different size Surface and Rect")

surface = pygame.Surface((100, 100))
surface.fill("red")

rectsurf = pygame.Surface((50, 50))
rectsurf.fill("pink")

rect = rectsurf.get_rect()
rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	
	screen.fill("black")
	
	screen.blit(surface, rect)
	screen.blit(rectsurf, rect)
	pygame.display.update()