import pygame, sys
from scene import Scene
from player import Player
from all_sprites import AllSprites
from objects import load_assets_str_list
from settings import *
from objects import SimpleSprite, LongSprite
from random import choice, randint
from car import Car
from game_util import make_text
from button import Button
import main_menu_scene

class GameScene(Scene):
    def __init__(self) -> None:
        super(GameScene, self).__init__()

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.button_group = pygame.sprite.Group()
        self.button_group_victory = pygame.sprite.Group()
        self.button_group_lose = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.player = Player((2062,3274), self.all_sprites, self.collision_sprites)

        # background and foreground
        self.bg = pygame.image.load('./graphics/main/map.png').convert()
        self.fg = pygame.image.load('./graphics/main/overlay.png').convert_alpha()
        
                # # objects sprites
        objects_list_simple = load_assets_str_list('./graphics/objects/simple')
        objects_list_long = load_assets_str_list('./graphics/objects/long')

        self.scene_dt = 0.0
        self.is_paused = False

        Button(
            (WINDOW_WIDTH/2, WINDOW_HEIGHT/2.3),
            'Main Menu',
            [self.button_group,self.button_group_victory,self.button_group_lose],
            lambda: self.GoToScene(main_menu_scene.MenuScene())
            )

        Button(
            (WINDOW_WIDTH/2, WINDOW_HEIGHT/2),
            'Return',
            self.button_group,
            lambda: self.toggle_pause(False)
            )

        Button(
            (WINDOW_WIDTH/2, WINDOW_HEIGHT/2),
            'Restart',
            self.button_group_lose,
            lambda: self.restart_game()
            )

        for sett in SIMPLE_OBJECTS:
            for pos in SIMPLE_OBJECTS[sett]:
                SimpleSprite(objects_list_simple[sett], pos, [self.all_sprites, self.collision_sprites])

        for sett in LONG_OBJECTS:
            for pos in LONG_OBJECTS[sett]:
                LongSprite(objects_list_long[sett], pos, [self.all_sprites, self.collision_sprites])

        self.car_timer = pygame.event.custom_type()
        pygame.time.set_timer(self.car_timer, 60)
        self.car_pos_list = []


    def restart_game(self):
        self.GoToScene(GameScene())


    def render(self, screen):
        self.all_sprites.customizeDraw(self.player, screen, self.bg, self.fg)

        # if paused
        if self.is_paused:
            self.pause_menu(screen)

        # check victory condition
        if self.player.has_won:
            self.toggle_pause(True)
            self.victory_menu(screen)

        # check lose condition
        if self.player.has_hit:
            self.toggle_pause(True)
            self.lose_menu(screen)

    def victory_menu(self,screen):
        color = 'red'
        pygame.draw.rect(
            screen,
            color,
            pygame.rect.Rect(WINDOW_WIDTH/4,WINDOW_HEIGHT/4,WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        )

        [self.text_surface_pause, self.text_rectangle_pause] = make_text('VICTORY!',(WINDOW_WIDTH/2, WINDOW_HEIGHT/3))
        
        screen.blit(self.text_surface_pause,self.text_rectangle_pause)
        self.button_group_victory.draw(screen)
        self.button_group_victory.update(None)

    def lose_menu(self,screen):
        color = 'black'
        pygame.draw.rect(
            screen,
            color,
            pygame.rect.Rect(WINDOW_WIDTH/4,WINDOW_HEIGHT/4,WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        )

        [self.text_surface_pause, self.text_rectangle_pause] = make_text('YOU LOSE!',(WINDOW_WIDTH/2, WINDOW_HEIGHT/3))
        
        screen.blit(self.text_surface_pause,self.text_rectangle_pause)
        self.button_group_lose.draw(screen)
        self.button_group_lose.update(None)

    def pause_menu(self,screen):
        color = 'teal'
        pygame.draw.rect(
            screen,
            color,
            pygame.rect.Rect(WINDOW_WIDTH/4,WINDOW_HEIGHT/4,WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        )

        [self.text_surface_pause, self.text_rectangle_pause] = make_text('Paused',(WINDOW_WIDTH/2, WINDOW_HEIGHT/3))
        

        screen.blit(self.text_surface_pause,self.text_rectangle_pause)
        self.button_group.draw(screen)
        self.button_group.update(None)

    def update(self,dt):
        if not self.is_paused:
            self.all_sprites.update(dt)


    def toggle_pause(self, value = None):
        if value == None:
            self.is_paused = not self.is_paused
        else:
            self.is_paused = value

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            # toggle pause
            if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                self.toggle_pause()

            if e.type == self.car_timer:
                random_pos = choice(CAR_START_POSITIONS)

                if random_pos not in self.car_pos_list:
                    self.car_pos_list.append(random_pos)
                    randomized_pos = (random_pos[0],random_pos[1]+ randint(-8,8))
                    Car((randomized_pos),[self.all_sprites, self.collision_sprites],self.bg.get_size()[0])
                if len(self.car_pos_list) > 5:
                    del self.car_pos_list[0]

        if self.is_paused and not self.player.has_hit:
            for sp in self.button_group:
                if hasattr(sp,'handle_event'):
                    sp.handle_event(events)

        if self.is_paused and self.player.has_hit:
            for sp in self.button_group_lose:
                if hasattr(sp,'handle_event'):
                    sp.handle_event(events)

