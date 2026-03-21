import pygame
import time
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("TypeTarzan")
clock = pygame.time.Clock()
scroll = 0
car_speed = 3 


road_surface = pygame.image.load('assets/road.jpeg').convert()
road_surface = pygame.transform.scale(road_surface, (1000, 600))
road_height = 600

text_bg = pygame.image.load('assets/text_bg.png').convert_alpha()
text_bg = pygame.transform.scale(text_bg, (1400, 450))
text_bg_rect = text_bg.get_rect(center = (500, 66))

font = pygame.font.SysFont("Consolas", 40)
target_text = "type this text as fast as you can"
user_input = ""
text_surface = font.render(target_text, True, (28, 26, 1))

typing_start_time = None
last_typed_time = None
wpm = 0
decrease_speed_after_interval = 1.5 # cars speed will slow down after this much time of inactivity
decrease_speed_rate = 0.8

def calculate_wpm(start_time, char_typed):
    elapsed_mins = (time.time() - start_time)
    if elapsed_mins == 0:
        return 0
    words_typed = char_typed / 5 # 5 characters = 1 word
    return words_typed / elapsed_mins

def wpm_to_speed(wpm): return wpm/1 # The entire game is 60fps, if the return raw wpm as speed then the car will go out of screen


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
                if typing_start_time is None:
                    typing_start_time = time.time()
                user_input += event.text
                last_typed_time = time.time()

                wpm = calculate_wpm (typing_start_time, len(user_input))


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
                last_typed_time = time.time()
    
    if last_typed_time is not None:
        idle_time = time.time() - last_typed_time 
        if idle_time > decrease_speed_after_interval:
            wpm *= decrease_speed_rate
    
    car_speed = wpm_to_speed(wpm)

    scroll += car_speed
    if scroll >= road_height:
        scroll -= road_height

    screen.blit(road_surface, (0, scroll))
    screen.blit(road_surface, (0, scroll - road_height))

    screen.blit(car1_surface, car1_rect)
    screen.blit(car2_surface, car2_rect)

    screen.blit(text_bg, text_bg_rect)
    # screen.blit(text_surface, (130, 50))

    def validate_text():
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
    
    validate_text()
    wpm_surface = font.render(f"WPM: {int(wpm)}", True, (255,255,255))
    screen.blit(wpm_surface, (40, 540))

    pygame.display.update()
    clock.tick(60)