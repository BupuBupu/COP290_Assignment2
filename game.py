import pygame
import sys

pygame.init()

screen_width = 1504
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Naughty Kids")


game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    pygame.display.flip()

pygame.quit()
sys.exit() 
