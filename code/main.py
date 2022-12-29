import pygame, sys, copy

from random import choice, randint
from settings import *
from player import Player
from car import Car
from main_menu_scene import MenuScene

def main():

    # basic setup
    pygame.init()
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Frogger')
    clock = pygame.time.Clock()

    # music
    music = pygame.mixer.Sound('./audio/music.mp3')
    music.play(loops=-1)

    # font
    font = pygame.font.Font(None, 50)
    text_surface = font.render('You Won!',True, 'White')
    text_rectangle = text_surface.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

    # scene = GameScene()
    current_scene = MenuScene()

    exit_game = False

    # game loop
    while not exit_game:

        # anything has to be set before pygame.event.get(QUIT) so it can work
        dt = clock.tick() / 1000 # getting in seconds, limit by 60

        if pygame.event.get(pygame.QUIT):
            exit_game = True
            return

        current_scene.handle_events(pygame.event.get())
        current_scene.update(dt)
        display_surface.fill('black')

        current_scene.render(display_surface)

        if current_scene != current_scene.next_scene:
            current_scene = current_scene.next_scene

        # clear bg
        pygame.display.update()

        
    pygame.display.quit()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()