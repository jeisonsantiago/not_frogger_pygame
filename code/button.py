import pygame
from game_util import make_text

COLOR_FILL = (192,192,192)
COLOR_HOVER_FILL = (128,128,128)
WIDTH = 200
HEIGHT = 30


class Button(pygame.sprite.Sprite):
    def __init__(self,pos,text,groups, func = None) -> None:
        super().__init__(groups)

        self.text = text
        self.func = func
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(COLOR_FILL)
        self.rect = self.image.get_rect(center=pos)

        font = pygame.font.Font(None, 40)
        self.text_surface = font.render(text,True,'black')


    def update(self,dt):

        # mouse hover
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse[0],mouse[1]):
            self.image.fill(COLOR_HOVER_FILL)
        else:
            self.image.fill(COLOR_FILL)

        self.image.blit(
            self.text_surface, 
            [WIDTH/2 - self.text_surface.get_width()/2,HEIGHT/2 - self.text_surface.get_height()/2])
        
    def handle_event(self,event):
        for e in event:
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.rect.collidepoint(mouse[0],mouse[1]):
                    if self.func != None:
                        self.func()
