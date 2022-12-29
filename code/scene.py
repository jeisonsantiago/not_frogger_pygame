import pygame

class Scene(object):
    def __init__(self) -> None:
        self.next_scene = self

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError
    
    def handle_events(self,events):
        raise NotImplementedError

    def GoToScene(self, next_scene):
        self.next_scene = next_scene

    def Terminate(self):
        self.GoToScene(None)