import pygame
DIFFICULTY_SETTINGS = {
    "easy":   {"computer_speed": 2},
    "medium": {"computer_speed": 4},
    "hard":   {"computer_speed": 7},
}
class GameEngine:
    FINISH_LINE_Y = 80
    START_Y = 470
    def __init__(self, player, player_car, computer_car, difficulty):
        self.player = player
        self.player_car = player_car
        self.computer_car = computer_car
        self.difficulty = difficulty
        settings = DIFFICULTY_SETTINGS[difficulty]
        self.computer_car.speed = settings["computer_speed"]
        self.road_surface = None
        self.road_height = 600
        self.scroll = 0
        self.winner = None 
        self.running = False
    def set_road(self, road_surface):
        self.road_surface = road_surface
    def start(self):
        self.player.reset()
        self.player_car.reset()
        self.computer_car.reset()
        self.computer_car.speed = DIFFICULTY_SETTINGS[self.difficulty]["computer_speed"]
        self.scroll  = 0
        self.winner  = None
        self.running = True
    def update(self):
        if not self.running:
            return
        self.player.apply_idle_decay()
        max_speed = DIFFICULTY_SETTINGS[self.difficulty]["computer_speed"] * 3
        self.player_car.speed = min(self.player.get_speed(), max_speed)
        self.player_car.speed = self.player.get_speed()
        self.player_car.move()
        self.computer_car.move()
        avg_speed = (self.player_car.speed + self.computer_car.speed) / 2
        self.scroll = (self.scroll + avg_speed) % self.road_height
        if self.player_car.has_won():
            self.winner = "player"
            self.running = False
        elif self.computer_car.has_won():
            self.winner = "computer"
            self.running = False
    def draw_road(self, screen):
        if self.road_surface:
            screen.blit(self.road_surface, (0, self.scroll - self.road_height))
            screen.blit(self.road_surface, (0, self.scroll))
    def draw_finish_line(self, screen):
        pygame.draw.line(screen, (255, 255, 255), (0, self.FINISH_LINE_Y), (1000, self.FINISH_LINE_Y), 3)
        font = pygame.font.SysFont("Consolas", 20)
        label = font.render("FINISH", True, (255, 255, 255))
        screen.blit(label, (10, self.FINISH_LINE_Y - 22))
    def is_over(self):
        return self.winner is not None