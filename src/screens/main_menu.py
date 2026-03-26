import pygame
from src.screens.base_screen import BaseScreen
class MainMenu(BaseScreen):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.font_title = pygame.font.SysFont("Consolas", 60, bold=True)
        self.font_option = pygame.font.SysFont("Consolas", 36)
        self.options = ["Play", "High Scores", "Quit"]
        self.selected = 0
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: self.selected = (self.selected - 1) % len(self.options)
                if event.key == pygame.K_DOWN: self.selected = (self.selected + 1) % len(self.options)
                if event.key == pygame.K_RETURN: self._select()
    def _select(self):
        if self.options[self.selected] == "Play": self.next_screen = "difficulty"
        elif self.options[self.selected] == "High Scores": self.next_screen = "highscores"
        elif self.options[self.selected] == "Quit": self.next_screen = "exit"
    def draw(self):
        self.screen.fill((15, 15, 25))
        title = self.font_title.render("TypeTarzan", True, (255, 220, 50))
        self.screen.blit(title, title.get_rect(center=(500, 130)))
        pygame.draw.line(self.screen, (255, 220, 50), (300, 175), (700, 175), 2)
        for i, option in enumerate(self.options):
            color = (255, 220, 50) if i == self.selected else (180, 180, 180)
            prefix = "> " if i == self.selected else "   "
            surf = self.font_option.render(prefix + option, True, color)
            rect = surf.get_rect(center=(500, 260 + i * 70))
            self.screen.blit(surf, rect)