import pygame
import sys
import button
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Sprout land')

#Game variables
game_paused = False


#define fonts
font = pygame.font.SysFont("arialblack", 40)

TEXT_COLOR = (255,255,255)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

clock = pygame.time.Clock()
run = True
while run:
    screen.fill((52,78,91))

    
    if game_paused:
        draw_text("Game Paused", font, TEXT_COLOR, 100, 300)
    else:
        draw_text("Press space to start", font, TEXT_COLOR, 100, 200)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = not game_paused

        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()