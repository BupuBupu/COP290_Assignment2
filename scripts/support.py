from os import walk
import pygame

def import_folder(path, zoom_factor, colorkey=(255, 255, 255)):
    surf_list = []
    for _, __, img_files in walk(path):
        img_files = sorted(img_files) # Linux issues
        for img in img_files:
            full_path = path + "/" + img
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.scale(image_surf, (image_surf.get_width()*zoom_factor, image_surf.get_height()*zoom_factor))
            if(colorkey is not None):
                image_surf.set_colorkey(colorkey)
            surf_list.append(image_surf)
    
    return surf_list