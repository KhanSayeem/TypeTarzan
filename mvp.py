import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("TypeTarzan")
clock = pygame.time.Clock()
road_surface = pygame.image.load('assets/road.jpeg').convert()
road_surface = pygame.transform.scale(road_surface, (1000,600))
car1_surface = pygame.image.load('assets/car1.png').convert_alpha()
car1_surface = pygame.transform.scale(car1_surface, (100,100))    
car1_rect = car1_surface.get_rect(center = (545,470))
car2_surface = pygame.image.load('assets/car2.png').convert_alpha()
car2_surface = pygame.transform.scale(car2_surface, (100,100))    
car2_rect = car1_surface.get_rect(center = (470,470))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(road_surface, (0,0))
    screen.blit(car1_surface, car1_rect)
    screen.blit(car2_surface, car2_rect)
    pygame.display.update()
    clock.tick(60)
