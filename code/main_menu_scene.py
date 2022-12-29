import pygame, sys
from scene import Scene
from settings import *
from game_util import make_text, quit_all
from button import Button
import game_scene

def changeScene(scene, newScene):
    scene.next_scene = newScene

class MenuScene(Scene):
    def __init__(self) -> None:
        super(MenuScene, self).__init__()

        self.all_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()
        
        [self.text_main_menu, self.text_rectangle_main_menu] = make_text('NOT FROGGER...',(WINDOW_WIDTH/2, WINDOW_HEIGHT/3),70)
        [self.text_play_game_menu, self.text_play_game_rectangle_menu] = make_text('Play Game',(WINDOW_WIDTH/2, WINDOW_HEIGHT/2.3))
        [self.text_quit_game_menu, self.text_play_quit_rectangle_menu] = make_text('Quit Game',(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

        Button(
            (WINDOW_WIDTH/2, WINDOW_HEIGHT/2.3),
            'Play',
            self.all_sprites,
            lambda: changeScene(self,game_scene.GameScene()) # this is necessary because lambdas cant do assignment
            )

        Button(
            (WINDOW_WIDTH/2, WINDOW_HEIGHT/2),
            'Quit',
            self.all_sprites,
            lambda: quit_all()
            )

    def render(self, screen):
        screen.fill('teal')
        self.all_sprites.draw(screen)
        screen.blit(self.text_main_menu, self.text_rectangle_main_menu)
        
    def update(self,dt):
        self.all_sprites.update(dt)


    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
        for sp in self.all_sprites:
            if hasattr(sp,'handle_event'):
                sp.handle_event(events)
        