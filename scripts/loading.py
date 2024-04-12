import pygame, sys, threading

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Loading screen')
FONT = pygame.font.SysFont("Roboto", 30)
CLOCK = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("#0d0e2e")
    pygame.display.update()
    CLOCK.tick(60)