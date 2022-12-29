import pygame
from os import walk
import re

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):

        super().__init__(groups)

        # import all images
        self.import_assets()
        self.frame_index = 0
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.collider = self.rect.inflate(0,-self.rect.height/2)
        
        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200

        # collisions
        self.collision_sprites = collision_sprites 

        self.has_won = False
        self.has_hit = False
    
    def import_assets(self):
        path = './graphics/player/right/'
        self.animation = []

        for frame in range(4):
            surf = pygame.image.load(f'{path}{frame}.png').convert_alpha()
            self.animation.append(surf)

        self.animations = dict()
        for index,folder in enumerate(walk('./graphics/player')):
            if index != 0:
                key = re.findall('([a-z]{1,})',folder[0])[-1]
                files = folder[-1]

                surface_files = []
                for file in files:
                    surface_files.append(pygame.image.load(f'{folder[0]}/{file}').convert_alpha())
                    self.animations[key] = surface_files
                

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites.sprites():
                if sprite.collider.colliderect(self.collider):
                    if hasattr(sprite,'name') and sprite.name == 'car':
                        self.has_hit = True
                    if self.direction.x > 0: # moving right
                        self.collider.right = sprite.collider.left
                        self.pos.x = self.collider.centerx
                    if self.direction.x < 0: # moving right
                        self.collider.left = sprite.collider.right
                        self.pos.x = self.collider.centerx
        else:
            for sprite in self.collision_sprites.sprites():
                if sprite.collider.colliderect(self.collider):
                    if hasattr(sprite,'name') and sprite.name == 'car':
                        self.has_hit = True
                    if self.direction.y > 0: # moving down
                        self.collider.bottom = sprite.collider.top
                        self.pos.y = self.collider.centery
                    if self.direction.y < 0: # moving up
                        self.collider.top = sprite.collider.bottom
                        self.pos.y = self.collider.centery
        

    def move(self,dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            
        # horizontal movement + collision
        self.pos.x += self.direction.x * self.speed * dt
        self.collider.centerx = round(self.pos.x)
        self.rect.centerx = self.collider.centerx
        self.collision('horizontal')

        # vertical movement + collision
        self.pos.y += self.direction.y * self.speed * dt
        self.collider.centery = round(self.pos.y)
        self.rect.centery = self.collider.centery
        self.collision('vertical')


    def input(self):
        keys = pygame.key.get_pressed()

        # horizontal input
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0.0

        # vertical input
        if keys[pygame.K_DOWN]:
            self.direction.y = 1
        elif keys[pygame.K_UP]:
            self.direction.y = -1
        else:
            self.direction.y = 0.0


    def animate(self,dt):

        if self.direction.x == 1:
            self.animation = self.animations['right']
        elif self.direction.x == -1:
            self.animation = self.animations['left']

        if self.direction.y == 1:
            self.animation = self.animations['down']
        elif self.direction.y == -1:
            self.animation = self.animations['up']

        if self.direction.magnitude() != 0:
            self.frame_index += 10 * dt

        if self.frame_index >= len(self.animation):
            self.frame_index = 0

        self.image = self.animation[int(self.frame_index)]

    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.collider.left = 640
            self.rect.left = 640
        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.collider.right = 2560
            self.rect.right = 2560
        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.collider.centery = self.rect.centery
        
        if self.rect.top < 1196:
            self.has_won = True

    def update(self,dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.restrict()