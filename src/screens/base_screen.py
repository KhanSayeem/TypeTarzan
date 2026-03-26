import pygame
class BaseScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.next_screen = None
    def handle_events(self, events):
        pass
    def update(self):
        pass
    def draw(self):
        pass