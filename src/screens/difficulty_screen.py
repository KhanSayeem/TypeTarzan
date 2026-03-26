import pygame
from src.screens.base_screen import BaseScreen
DIFFICULTY_INFO = {
    "easy":   {"label": "Easy",   "color": (80, 220, 100),  "desc": "Slow computer  |  Short text"},
    "medium": {"label": "Medium", "color": (255, 200, 50),  "desc": "Medium speed   |  Medium text"},
    "hard":   {"label": "Hard",   "color": (220, 60,  60),  "desc": "Fast computer  |  Long text"},
}
class DifficultyScreen(BaseScreen):
    def __init__(self, screen, clock, text_manager):
        super().__init__(screen, clock)
        self.text_manager = text_manager
        self.font_title  = pygame.font.SysFont("Consolas", 52, bold=True)
        self.font_option = pygame.font.SysFont("Consolas", 38)
        self.font_desc   = pygame.font.SysFont("Consolas", 22)
        self.options  = ["easy", "medium", "hard"]
        self.selected = 1  
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: self.selected = (self.selected - 1) % len(self.options)
                if event.key == pygame.K_DOWN: self.selected = (self.selected + 1) % len(self.options)
                if event.key == pygame.K_RETURN:
                    difficulty = self.options[self.selected]
                    self.text_manager.set_difficulty(difficulty)
                    self.next_screen = "textselect"
                if event.key == pygame.K_ESCAPE: self.next_screen = "menu"
    def draw(self):
        self.screen.fill((15, 15, 25))
        title = self.font_title.render("Select Difficulty", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(500, 100)))
        pygame.draw.line(self.screen, (100, 100, 100), (200, 145), (800, 145), 2)
        for i, key in enumerate(self.options):
            info      = DIFFICULTY_INFO[key]
            is_sel    = i == self.selected
            color     = info["color"] if is_sel else (130, 130, 130)
            prefix    = ">  " if is_sel else "   "
            if is_sel:
                box = pygame.Rect(220, 195 + i * 110 - 10, 560, 85)
                pygame.draw.rect(self.screen, (30, 30, 45), box, border_radius=8)
                pygame.draw.rect(self.screen, info["color"], box, 2, border_radius=8)
            label = self.font_option.render(prefix + info["label"], True, color)
            self.screen.blit(label, label.get_rect(midleft=(240, 195 + i * 110 + 20)))
            desc  = self.font_desc.render(info["desc"], True, (150, 150, 150) if not is_sel else (200, 200, 200))
            self.screen.blit(desc, desc.get_rect(midleft=(280, 195 + i * 110 + 55)))
        hint = self.font_desc.render("ESC: back to menu", True, (100, 100, 100))
        self.screen.blit(hint, hint.get_rect(center=(500, 570)))