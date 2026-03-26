import pygame
from src.screens.base_screen import BaseScreen
DIFF_COLORS = {
    "easy":   (80, 220, 100),
    "medium": (255, 200, 50),
    "hard":   (220, 60, 60),
}
class HighScoresScreen(BaseScreen):
    def __init__(self, screen, clock, storage):
        super().__init__(screen, clock)
        self.storage = storage
        self.font_title = pygame.font.SysFont("Consolas", 48, bold=True)
        self.font_header = pygame.font.SysFont("Consolas", 22, bold=True)
        self.font_row = pygame.font.SysFont("Consolas", 22)
        self.font_small = pygame.font.SysFont("Consolas", 20)
        self.scores = []
    def on_enter(self):
        self.scores = self.storage.get_high_scores()
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    self.next_screen = "menu"
    def draw(self):
        self.screen.fill((15, 15, 25))
        title = self.font_title.render("High Scores", True, (255, 220, 50))
        self.screen.blit(title, title.get_rect(center=(500, 50)))
        pygame.draw.line(self.screen, (60, 60, 80), (100, 90), (900, 90), 2)
        if not self.scores:
            msg = self.font_row.render("No scores yet. Play a race first!", True, (150, 150, 150))
            self.screen.blit(msg, msg.get_rect(center=(500, 300)))
        else:
            headers = ["#", "WPM", "Difficulty", "Result", "Date"]
            col_x = [80, 180, 310, 530, 700]
            for header, x in zip(headers, col_x):
                h = self.font_header.render(header, True, (120, 120, 120))
                self.screen.blit(h, (x, 105))
            pygame.draw.line(self.screen, (50, 50, 70), (70, 128), (930, 128), 1)
            for i, score in enumerate(self.scores):
                y = 138 + i * 38
                diff = score["difficulty"]
                result = score["result"]
                diff_color = DIFF_COLORS.get(diff, (200, 200, 200))
                res_color  = (80, 220, 100) if result == "win" else (220, 60, 60)
                row_data = [
                    (str(i + 1), (180, 180, 180), col_x[0]),
                    (str(score["wpm"]), (255, 255, 255), col_x[1]),
                    (diff.capitalize(), diff_color, col_x[2]),
                    (result.capitalize(), res_color, col_x[3]),
                    (score.get("date", "-"), (130, 130, 130), col_x[4]),
                ]
                for text, color, x in row_data:
                    s = self.font_row.render(text, True, color)
                    self.screen.blit(s, (x, y))
        hint = self.font_small.render("ESC or ENTER back to menu", True, (80, 80, 80))
        self.screen.blit(hint, hint.get_rect(center=(500, 575)))