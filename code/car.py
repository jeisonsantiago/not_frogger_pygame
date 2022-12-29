import pygame
from os import walk
import random
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

class Car(pygame.sprite.Sprite):
    def __init__(self, pos, groups, w_limit = 0):
        super().__init__(groups)
        
        self.name = 'car'

        self.import_asset()

        # image
        self.rect = self.image.get_rect(center = pos)
        self.collider = self.rect.inflate(0,-self.rect.height/2)
        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2(1,0)
        self.speed = 200 

        self.w_limit = w_limit

        if self.pos[0] < 200:
            self.direction = pygame.math.Vector2(1,0)
        else:
            self.direction = pygame.math.Vector2(-1,0)
            self.image = pygame.transform.flip(self.image,True, False)


    def import_asset(self):
        path = './graphics/cars'
        cars_files = []
        for file in (walk(path)):
            cars_files = file[-1]


        # select with car randomily
        random_index = random.randint(0,len(cars_files)-1)
        self.image = pygame.image.load(f'{path}/{cars_files[random_index]}').convert_alpha()
    
    def update(self,dt):
        self.pos += self.direction * self.speed * dt

        self.collider.center = (round(self.pos.x),round(self.pos.y))

        self.rect.center = self.collider.center



        # self delete queue_free()
        if (self.pos.x + self.rect.width) < 0 and self.direction.x == -1:
            self.kill()

        if (self.pos.x - self.rect.width) > self.w_limit and self.direction.x == 1:
            self.kill()