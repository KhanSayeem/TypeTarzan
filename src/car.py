import pygame
class Car:
    FINISH_LINE_Y = 80
    def __init__(self, image_path, x, y, speed=0):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.start_y = y
    def move(self):
        self.rect.y -= self.speed
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def has_won(self):
        return self.rect.y <= self.FINISH_LINE_Y
    def reset(self):
        self.rect.y = self.start_y
        self.speed = 0