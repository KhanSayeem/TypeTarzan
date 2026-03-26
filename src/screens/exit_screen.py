import pygame
from src.screens.base_screen import BaseScreen
class ExitScreen(BaseScreen):
    def __init__(self, screen, clock, storage):
        super().__init__(screen, clock)
        self.storage = storage
        self.font_title = pygame.font.SysFont("Consolas", 52, bold=True)
        self.font_stat  = pygame.font.SysFont("Consolas", 32)
        self.font_small = pygame.font.SysFont("Consolas", 22)
        self.stats = {}
        self.blink_timer = 0
        self.show_hint = True
    def on_enter(self):
        self.stats = self.storage.get_lifetime_stats()
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                raise SystemExit
    def update(self):
        self.blink_timer += self.clock.get_time()
        if self.blink_timer >= 600:
            self.show_hint = not self.show_hint
            self.blink_timer = 0
    def draw(self):
        self.screen.fill((15, 15, 25))
        title = self.font_title.render("Thanks for Playing!", True, (255, 220, 50))
        self.screen.blit(title, title.get_rect(center=(500, 90)))
        pygame.draw.line(self.screen, (60, 60, 80), (150, 140), (850, 140), 2)
        wins = self.stats.get("wins", 0)
        losses = self.stats.get("losses", 0)
        best_wpm = self.stats.get("best_wpm", 0)
        total = wins + losses
        win_rate = round((wins / total) * 100) if total > 0 else 0
        stats = [
            ("Races Played", str(total)),
            ("Wins", str(wins)),
            ("Losses", str(losses)),
            ("Win Rate", f"{win_rate}%"),
            ("Best WPM", str(best_wpm)),
        ]
        for i, (label, value) in enumerate(stats):
            label_surf = self.font_stat.render(label, True, (150, 150, 150))
            value_surf = self.font_stat.render(value, True, (255, 255, 255))
            y = 175 + i * 55
            self.screen.blit(label_surf, label_surf.get_rect(midright=(440, y)))
            self.screen.blit(value_surf, value_surf.get_rect(midleft=(470, y)))
        pygame.draw.line(self.screen, (60, 60, 80), (150, 460), (850, 460), 2)
        if self.show_hint:
            hint = self.font_small.render("Press any key to exit", True, (120, 120, 120))
            self.screen.blit(hint, hint.get_rect(center=(500, 490)))