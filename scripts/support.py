from os import walk, listdir
import pygame

def import_folder(path, zoom_factor):
    surface_list = []
    print(path)
    print(listdir(path))
    for _, __, img_files in walk(path):
        print(img_files)
        img_files = sorted(img_files) # Linux problems
        for img in img_files:
            full_path = path + "/" + img
            print("puppy:",img)
            image_surf = pygame.image.load(full_path).convert_alpha() # converting to something which is easier to work with in pygame, so code run fast boom and we get boom
            image_surf = pygame.transform.scale(image_surf, (image_surf.get_width()*zoom_factor, image_surf.get_height()*zoom_factor))
            image_surf.set_colorkey((255, 255, 255))
            surface_list.append(image_surf)
    
    return surface_list