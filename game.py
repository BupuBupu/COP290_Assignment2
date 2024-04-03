import pygame
import sys

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

from pytmx.util_pygame import load_pygame

pygame.init()

screen_width = 1504
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
tmx_data = load_pygame("./assets/tilesets/Map/Map.tmx")
pygame.display.set_caption("Naughty Kids")
sprite_group = pygame.sprite.Group()



# cycle through layers

for layer in tmx_data.layers:
    if hasattr(layer, 'data'):
        for x,y,surf in layer.tiles():
            pos = (x*16, y*16)
            Tile(pos,surf,sprite_group)

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    sprite_group.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit() 
