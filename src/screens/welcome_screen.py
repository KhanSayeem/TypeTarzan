import pygame
from src.screens.base_screen import BaseScreen
class WelcomeScreen(BaseScreen):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.font_title = pygame.font.SysFont("Consolas", 72, bold=True)
        self.font_sub   = pygame.font.SysFont("Consolas", 30)
        self.title_surf  = self.font_title.render("TypeTarzan", True, (255, 220, 50))
        self.sub_surf    = self.font_sub.render("Press ENTER to start", True, (200, 200, 200))
        self.title_rect  = self.title_surf.get_rect(center=(500, 230))
        self.sub_rect    = self.sub_surf.get_rect(center=(500, 340))
        self.blink_timer = 0
        self.show_sub    = True
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_screen = "menu"
    def update(self):
        self.blink_timer += self.clock.get_time()
        if self.blink_timer >= 500:
            self.show_sub    = not self.show_sub
            self.blink_timer = 0
    def draw(self):
        self.screen.fill((15, 15, 25))
        pygame.draw.line(
            self.screen,
            (255, 220, 50),
            (200, 275), (800, 275), 2
        )
        self.screen.blit(self.title_surf, self.title_rect)
        if self.show_sub:
            self.screen.blit(self.sub_surf, self.sub_rect)