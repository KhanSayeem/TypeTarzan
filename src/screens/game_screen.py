import pygame
from src.screens.base_screen import BaseScreen
from src.engine import GameEngine
from src.player import Player
from src.car import Car
class GameScreen(BaseScreen):
    def __init__(self, screen, clock, text_manager, storage):
        super().__init__(screen, clock)
        self.text_manager = text_manager
        self.storage = storage
        self.font_ui = pygame.font.SysFont("Consolas", 28)
        self.font_text = pygame.font.SysFont("Consolas", 26)
        self.font_small = pygame.font.SysFont("Consolas", 20)
        self.COLOR_CORRECT = (80, 220, 100)
        self.COLOR_INCORRECT = (220, 60, 60)
        self.COLOR_PENDING = (200, 200, 200)
        self.player = None
        self.engine = None
        self.target_text = None
        self.difficulty = None
        self.text_box = pygame.Rect(0, 540, 1000, 60)
    def on_enter(self):
        self.target_text = self.text_manager.get_text()
        self.difficulty  = self.text_manager.difficulty
        self.player = Player()
        road = pygame.image.load("assets/road.jpeg").convert()
        road = pygame.transform.scale(road, (1000, 600))
        player_car   = Car("assets/car1.png", x=545, y=470)
        computer_car = Car("assets/car2.png", x=455, y=470)
        self.engine = GameEngine(
            self.player, player_car, computer_car, self.difficulty
        )
        self.engine.set_road(road)
        self.engine.start()
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_screen = "menu"
            self.player.handle_keypress(event, self.target_text)
    def update(self):
        self.engine.update()
        if self.engine.is_over():
            result = "win" if self.engine.winner == "player" else "loss"
            self.storage._add_result(
                wpm = int(self.player.wpm),
                difficulty = self.difficulty,
                result = result
            )
            self.next_screen = "result"
    def draw(self):
        self.engine.draw_road(self.screen)
        self.engine.draw_finish_line(self.screen)
        self.engine.player_car.draw(self.screen)
        self.engine.computer_car.draw(self.screen)
        pygame.draw.rect(self.screen, (15, 15, 25), self.text_box)
        pygame.draw.line(self.screen, (60, 60, 80), (0, 540), (1000, 540), 2)
        self._draw_target_text()
        wpm_surf = self.font_ui.render(f"WPM: {int(self.player.wpm)}", True, (255, 220, 50))
        self.screen.blit(wpm_surf, (20, 545))
        esc = self.font_small.render("ESC — quit race", True, (80, 80, 80))
        self.screen.blit(esc, (820, 578))
    def _draw_target_text(self):
        x_start = 20
        y_start = 548
        x = x_start
        max_width = 760
        for i, char in enumerate(self.target_text):
            if i < len(self.player.user_input):
                color = (
                    self.COLOR_CORRECT
                    if self.player.user_input[i] == char
                    else self.COLOR_INCORRECT
                )
            else:
                color = self.COLOR_PENDING
            char_surf = self.font_text.render(char, True, color)
            char_w = char_surf.get_width()

            if x + char_w > x_start + max_width:
                x = x_start
                y_start += 28
            self.screen.blit(char_surf, (x, y_start))
            x += char_w