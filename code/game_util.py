import pygame,sys

def make_text(text_str, pos, font_size = 50,color = 'white'):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text_str,True,color)
    text_rectangle = text_surface.get_rect(center=pos)

    return [text_surface, text_rectangle]

def quit_all():
    pygame.display.quit()
    pygame.quit()
    sys.exit()
