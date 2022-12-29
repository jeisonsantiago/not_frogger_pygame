import pygame
from os import walk
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, url, pos, groups):
        super().__init__(groups)

        # image
        self.image = pygame.image.load(url).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.collider = self.rect.inflate(0,-self.rect.height/2)
        self.collider.bottom =  self.rect.bottom
    
class LongSprite(pygame.sprite.Sprite):
    def __init__(self, url, pos, groups):
        super().__init__(groups)
        
        # image
        self.image = pygame.image.load(url).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.collider = self.rect.inflate(-self.rect.width * 0.8, -self.rect.height/2)
        

def load_assets_str_list(url, settings_list_positions = []):

    file_list = dict()
    for files in walk(url):
        for file in files[-1]:
            key = str.removesuffix(file,'.png')
            # file_list[key] = pygame.image.load(f'{url}/{file}').convert_alpha()
            file_list[key] = f'{url}/{file}'

    return file_list



    
        
