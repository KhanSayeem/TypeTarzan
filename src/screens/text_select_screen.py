import pygame
from src.screens.base_screen import BaseScreen
class TextSelectScreen(BaseScreen):
    def __init__(self, screen, clock, text_manager):
        super().__init__(screen, clock)
        self.text_manager = text_manager
        self.font_title = pygame.font.SysFont("Consolas", 46, bold=True)
        self.font_tab = pygame.font.SysFont("Consolas", 30, bold=True)
        self.font_option = pygame.font.SysFont("Consolas", 24)
        self.font_small = pygame.font.SysFont("Consolas", 20)
        self.active_tab = 0
        self.selected = 0
        self.custom_input = ""
        self.error_message = ""
        self.blink_timer = 0
        self.show_cursor = True
    def on_enter(self):
        self.selected = 0
        self.custom_input = ""
        self.error_message = ""
        self.active_tab = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.active_tab   = (self.active_tab + 1) % 2
                    self.error_message = ""
                elif event.key == pygame.K_ESCAPE:
                    self.next_screen = "difficulty"
                elif self.active_tab == 0:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self._presets())
                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self._presets())
                    if event.key == pygame.K_RETURN:
                        self.text_manager.select_preset(self.selected)
                        self.next_screen = "game"
                elif self.active_tab == 1:
                    if event.key == pygame.K_BACKSPACE:
                        self.custom_input  = self.custom_input[:-1]
                        self.error_message = ""
                    elif event.key == pygame.K_RETURN:
                        ok, msg = self.text_manager.set_custom(self.custom_input)
                        if ok:
                            self.next_screen = "game"
                        else:
                            self.error_message = msg
            if event.type == pygame.TEXTINPUT and self.active_tab == 1:
                if len(self.custom_input) < 120:
                    self.custom_input += event.text
    def update(self):
        self.blink_timer += self.clock.get_time()
        if self.blink_timer >= 500:
            self.show_cursor= not self.show_cursor
            self.blink_timer = 0
    def draw(self):
        self.screen.fill((15, 15, 25))
        title = self.font_title.render("Choose Your Text", True, (255, 255, 255))
        self.screen.blit(title, title.get_rect(center=(500, 55)))
        self._draw_tabs()
        if self.active_tab == 0:
            self._draw_presets()
        else:
            self._draw_custom()
        hints = "TAB: switch tab   |   ESC: back   |   ENTER: confirm"
        hint_surf = self.font_small.render(hints, True, (100, 100, 100))
        self.screen.blit(hint_surf, hint_surf.get_rect(center=(500, 575)))
    def _presets(self):
        return self.text_manager.get_presets()
    def _draw_tabs(self):
        labels = ["  Presets  ", "  Custom  "]
        tab_colors = [(255, 220, 50), (100, 180, 255)]
        x = 280
        for i, label in enumerate(labels):
            is_active = i == self.active_tab
            color = tab_colors[i] if is_active else (100, 100, 100)
            surf = self.font_tab.render(label, True, color)
            rect = surf.get_rect(topleft=(x, 100))
            self.screen.blit(surf, rect)
            if is_active:
                pygame.draw.line(
                    self.screen, color,
                    (rect.left, rect.bottom + 2),
                    (rect.right, rect.bottom + 2), 2
                )
            x += 220
    def _draw_presets(self):
        presets = self._presets()
        if not presets:
            msg = self.font_option.render("No presets available.", True, (200, 100, 100))
            self.screen.blit(msg, msg.get_rect(center=(500, 300)))
            return
        for i, text in enumerate(presets):
            is_sel = i == self.selected
            color = (255, 220, 50) if is_sel else (180, 180, 180)
            prefix = ">  " if is_sel else "   "

            # Highlight box
            if is_sel:
                box = pygame.Rect(80, 155 + i * 100 - 8, 840, 70)
                pygame.draw.rect(self.screen, (30, 30, 45), box, border_radius=6)
                pygame.draw.rect(self.screen, (255, 220, 50), box, 2, border_radius=6)
            # Wrap long text across two lines
            words = (prefix + text).split()
            line1, line2 = "", ""
            for word in words:
                test = line1 + word + " "
                if self.font_option.size(test)[0] < 820:
                    line1 = test
                else:
                    line2 += word + " "
            y = 155 + i * 100
            s1 = self.font_option.render(line1.strip(), True, color)
            self.screen.blit(s1, s1.get_rect(midleft=(90, y + 15)))
            if line2.strip():
                s2 = self.font_option.render(line2.strip(), True, color)
                self.screen.blit(s2, s2.get_rect(midleft=(90, y + 42)))
    def _draw_custom(self):
        instr = self.font_option.render("Type your own text below:", True, (180, 180, 180))
        self.screen.blit(instr, instr.get_rect(midleft=(90, 160)))
        box = pygame.Rect(80, 200, 840, 160)
        pygame.draw.rect(self.screen, (25, 25, 40), box, border_radius=8)
        border_color = (200, 80, 80) if self.error_message else (100, 100, 180)
        pygame.draw.rect(self.screen, border_color, box, 2, border_radius=8)
        display_text = self.custom_input
        words = display_text.split()
        lines = []
        current_line = ""
        for word in words:
            test = current_line + word + " "
            if self.font_option.size(test)[0] < 800: current_line = test
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line)
        # Draw cursor on last line
        if self.show_cursor:
            lines[-1] += "|"
        for j, line in enumerate(lines[:4]):  # max 4 lines inside box
            ls = self.font_option.render(line, True, (230, 230, 230))
            self.screen.blit(ls, (95, 215 + j * 32))
        counter = self.font_small.render(
            f"{len(self.custom_input)}/120 characters", True, (120, 120, 120)
        )
        self.screen.blit(counter, counter.get_rect(bottomright=(915, 360)))
        if self.error_message:
            err = self.font_small.render(self.error_message, True, (220, 80, 80))
            self.screen.blit(err, err.get_rect(center=(500, 395)))
        reminder = self.font_small.render(
            "Minimum 10 characters. Press ENTER to confirm.", True, (100, 100, 100)
        )
        self.screen.blit(reminder, reminder.get_rect(center=(500, 430)))