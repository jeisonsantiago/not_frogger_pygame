import pygame, copy
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()

        self.debug_mode = False

    def customizeDraw(self, player,display_surface, background_sprite = None, foreground_sprite = None):

        # update offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # blit background
        if background_sprite != None:
            display_surface.blit(background_sprite,-self.offset)

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)
    
            # debug collider draw and update
            if self.debug_mode:
                color = (255,0,0)
                if hasattr(sprite,'collider'):
                    offset_pos_debug = sprite.collider.topleft - self.offset
                    debug_collider = copy.deepcopy(sprite.collider)
                    debug_collider.x = offset_pos_debug.x
                    debug_collider.y = offset_pos_debug.y
                    pygame.draw.rect(display_surface,color,debug_collider,2)
            
        # blit foreground overlay
        if foreground_sprite != None:
            display_surface.blit(foreground_sprite,-self.offset)
