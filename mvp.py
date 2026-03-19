import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("TypeTarzan")
clock = pygame.time.Clock()
scroll = 0
car_speed = 3 


road_surface = pygame.image.load('assets/road.jpeg').convert()
road_surface = pygame.transform.scale(road_surface, (1000, 600))
ROAD_H = 600

text_bg = pygame.image.load('assets/text_bg.png').convert_alpha()
text_bg = pygame.transform.scale(text_bg, (1400, 450))
text_bg_rect = text_bg.get_rect(center = (500, 66))

font = pygame.font.SysFont("Consolas", 40)
target_text = "Type this text as fast as you can"
user_input = ""
text_surface = font.render(target_text, True, (28, 26, 1))


# Player's car, its speed is determined by players typing speed.
car1_surface = pygame.image.load('assets/car1.png').convert_alpha()
car1_surface = pygame.transform.scale(car1_surface, (100, 100))
car1_rect = car1_surface.get_rect(center=(545, 470))

car2_surface = pygame.image.load('assets/car2.png').convert_alpha()
car2_surface = pygame.transform.scale(car2_surface, (100, 100))
car2_rect = car2_surface.get_rect(center=(470, 470)) 

correct_color = (0, 255, 0)
incorrect_color = (255,0,0)
incomplete_color = (28, 26, 1)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.TEXTINPUT:
            if len(user_input) < len(target_text):
                user_input += event.text


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]


    scroll += car_speed
    if scroll >= ROAD_H:
        scroll -= ROAD_H

    screen.blit(road_surface, (0, scroll))
    screen.blit(road_surface, (0, scroll - ROAD_H))

    screen.blit(car1_surface, car1_rect)
    screen.blit(car2_surface, car2_rect)

    screen.blit(text_bg, text_bg_rect)
    # screen.blit(text_surface, (130, 50))

    def validate_text_and_wpm():
            current_char = 110
            for i, char in enumerate(target_text):
                if i < len(user_input):
                    if user_input[i] == char:
                        color = correct_color
                        
                    else:
                        color = incorrect_color
                
                else:
                    color = incomplete_color

                char_surface = font.render(char, True, color)   
                screen.blit(char_surface, (current_char, 50)) 
                current_char += char_surface.get_width()         
    

    pygame.display.update()
    clock.tick(60)