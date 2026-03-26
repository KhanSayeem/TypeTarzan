import pygame
from src.screens.base_screen import BaseScreen
class ResultScreen(BaseScreen):
    def __init__(self, screen, clock, storage, text_manager):
        super().__init__(screen, clock)
        self.storage = storage
        self.text_manager = text_manager
        self.font_big = pygame.font.SysFont("Consolas", 72, bold=True)
        self.font_title = pygame.font.SysFont("Consolas", 36, bold=True)
        self.font_stat = pygame.font.SysFont("Consolas", 28)
        self.font_small = pygame.font.SysFont("Consolas", 22)
        self.winner = None
        self.wpm = 0
        self.accuracy = 0
        self.difficulty = None
        self.options = ["Play Again", "Main Menu", "Quit"]
        self.selected = 0
    def on_enter(self, engine, player):
        self.winner = engine.winner
        self.wpm = int(player.wpm)
        self.accuracy = player.get_accuracy(self.text_manager.get_text())
        self.difficulty = self.text_manager.difficulty
        self.selected = 0
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                if event.key == pygame.K_RETURN:
                    self._select()
    def _select(self):
        if self.options[self.selected] == "Play Again":
            self.next_screen = "difficulty"
        elif self.options[self.selected] == "Main Menu":
            self.next_screen = "menu"
        elif self.options[self.selected] == "Quit":
            self.next_screen = "exit"
    def draw(self):
        self.screen.fill((15, 15, 25))
        if self.winner == "player":
            headline      = "YOU WIN!"
            headline_color = (80, 220, 100)
        else:
            headline = "YOU LOSE!"
            headline_color = (220, 60, 60)
        hl = self.font_big.render(headline, True, headline_color)
        self.screen.blit(hl, hl.get_rect(center=(500, 100)))
        pygame.draw.line(self.screen, (60, 60, 80), (200, 155), (800, 155), 2)
        stats = [
            ("WPM", str(self.wpm)),
            ("Accuracy", f"{self.accuracy}%"),
            ("Difficulty", self.difficulty.capitalize()),
        ]
        for i, (label, value) in enumerate(stats):
            label_surf = self.font_stat.render(label, True, (150, 150, 150))
            value_surf = self.font_stat.render(value, True, (255, 255, 255))
            y = 190 + i * 50
            self.screen.blit(label_surf, label_surf.get_rect(midright=(460, y)))
            self.screen.blit(value_surf, value_surf.get_rect(midleft=(480, y)))
        pygame.draw.line(self.screen, (60, 60, 80), (200, 360), (800, 360), 2)
        for i, option in enumerate(self.options):
            is_sel = i == self.selected
            color  = (255, 220, 50) if is_sel else (150, 150, 150)
            prefix = "> " if is_sel else "   "
            surf   = self.font_stat.render(prefix + option, True, color)
            self.screen.blit(surf, surf.get_rect(center=(500, 400 + i * 55)))
        hint = self.font_small.render("ENTER to select", True, (80, 80, 80))
        self.screen.blit(hint, hint.get_rect(center=(500, 575)))