import pygame
from src.screens.base_screen import BaseScreen
diff_colors = {
    "easy":   (80, 220, 100),
    "medium": (255, 200, 50),
    "hard":   (220, 60,  60),
    "all":    (180, 180, 180),
}
class HighScoresScreen(BaseScreen):
    diff_options   = ["all", "easy", "medium", "hard"]
    result_options = ["all", "win", "loss"]
    sort_options   = ["wpm", "date"]
    def __init__(self, screen, clock, storage):
        super().__init__(screen, clock)
        self.storage = storage
        self.font_title = pygame.font.SysFont("Consolas", 44, bold=True)
        self.font_header = pygame.font.SysFont("Consolas", 20, bold=True)
        self.font_row = pygame.font.SysFont("Consolas", 20)
        self.font_small= pygame.font.SysFont("Consolas", 18)
        self.font_stat = pygame.font.SysFont("Consolas", 20)
        self.diff_index = 0 
        self.result_index = 0   
        self.sort_index = 0   
        self.sort_reverse = True
        self.selected_row = 0
        self.mode = "browse"
        self.scores = []
        self.stats  = {}
    def on_enter(self):
        self.diff_index = 0
        self.result_index = 0
        self.sort_index = 0
        self.sort_reverse = True
        self.selected_row = 0
        self.mode = "browse"
        self._refresh()
    def _refresh(self):
        diff = self.diff_options[self.diff_index]
        result = self.result_options[self.result_index]
        sort = self.sort_options[self.sort_index]
        raw  = self.storage.search_scores(difficulty=diff, result=result)
        self.scores = self.storage.sort_scores(raw, key=sort, reverse=self.sort_reverse)
        self.stats = self.storage.get_lifetime_stats()
        if self.scores:
            self.selected_row = min(self.selected_row, len(self.scores) - 1)
        else:
            self.selected_row = 0
    def handle_events(self, events):
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if self.mode == "confirm_delete":
                if event.key == pygame.K_y:
                    self._delete_selected()
                elif event.key in (pygame.K_n, pygame.K_ESCAPE):
                    self.mode = "browse"
                continue
            if event.key == pygame.K_ESCAPE:
                self.next_screen = "menu"
            elif event.key == pygame.K_d:
                self.diff_index   = (self.diff_index + 1) % len(self.diff_options)
                self.selected_row = 0
                self._refresh()
            elif event.key == pygame.K_r:
                self.result_index = (self.result_index + 1) % len(self.result_options)
                self.selected_row = 0
                self._refresh()
            elif event.key == pygame.K_s:
                self.sort_index   = (self.sort_index + 1) % len(self.sort_options)
                self._refresh()
            elif event.key == pygame.K_a:
                self.sort_reverse = not self.sort_reverse
                self._refresh()
            elif event.key == pygame.K_UP and self.scores:
                self.selected_row = (self.selected_row - 1) % len(self.scores)
            elif event.key == pygame.K_DOWN and self.scores:
                self.selected_row = (self.selected_row + 1) % len(self.scores)
            elif event.key == pygame.K_DELETE and self.scores:
                self.mode = "confirm_delete"
    def _delete_selected(self):
        if not self.scores:
            return
        score_id = self.scores[self.selected_row].get("id")
        self.storage.delete_score(score_id)
        self.mode = "browse"
        self._refresh()
    def draw(self):
        self.screen.fill((15, 15, 25))
        title = self.font_title.render("High Scores", True, (255, 220, 50))
        self.screen.blit(title, title.get_rect(center=(500, 30)))
        pygame.draw.line(self.screen, (60, 60, 80), (60, 60), (940, 60), 2)
        self._draw_filter_bar()
        self._draw_table()
        self._draw_summary()
        self._draw_hints()
        if self.mode == "confirm_delete":
            self._draw_confirm_overlay()
    def _draw_filter_bar(self):
        diff_color = diff_colors.get(self.diff_options[self.diff_index], (180,180,180))
        res_color  = (80, 220, 100) if self.result_options[self.result_index] == "win" \
                     else (220, 60, 60) if self.result_options[self.result_index] == "loss" \
                     else (180, 180, 180)
        sort_label = f"{self.sort_options[self.sort_index]} {'↓' if self.sort_reverse else '↑'}"
        items = [
            (f"[D] Difficulty: {self.diff_options[self.diff_index].capitalize()}",   diff_color),
            (f"[R] Result: {self.result_options[self.result_index].capitalize()}",   res_color),
            (f"[S] Sort: {sort_label}   [A] toggle order",                           (180, 180, 220)),
        ]
        x = 65
        for text, color in items:
            s = self.font_small.render(text, True, color)
            self.screen.blit(s, (x, 70))
            x += s.get_width() + 30
    def _draw_table(self):
        headers = ["#", "WPM", "Difficulty", "Result", "Date"]
        col_x  = [65, 130, 230, 430, 620]
        col_w = 860
        for header, x in zip(headers, col_x):
            h = self.font_header.render(header, True, (120, 120, 120))
            self.screen.blit(h, (x, 100))
        pygame.draw.line(self.screen, (50, 50, 70), (60, 120), (920, 120), 1)
        if not self.scores:
            msg = self.font_row.render("No scores match the current filter.", True, (150, 150, 150))
            self.screen.blit(msg, msg.get_rect(center=(500, 220)))
            return
        for i, score in enumerate(self.scores[:7]):
            y  = 128 + i * 34
            is_sel = i == self.selected_row
            if is_sel:
                pygame.draw.rect(self.screen, (30, 30, 50),
                                 pygame.Rect(58, y - 2, col_w, 28), border_radius=4)
                pygame.draw.rect(self.screen, (70, 70, 120),
                                 pygame.Rect(58, y - 2, col_w, 28), 1, border_radius=4)
            diff  = score["difficulty"]
            result  = score["result"]
            diff_col = diff_colors.get(diff, (200, 200, 200))
            res_col = (80, 220, 100) if result == "win" else (220, 60, 60)
            row = [
                (str(i + 1), (150, 150, 150), col_x[0]),
                (str(score["wpm"]), (255, 255, 255), col_x[1]),
                (diff.capitalize(),  diff_col, col_x[2]),
                (result.capitalize(), res_col, col_x[3]),
                (score.get("date","—"),(130, 130, 130), col_x[4]),
            ]
            for text, color, x in row:
                s = self.font_row.render(text, True, color)
                self.screen.blit(s, (x, y))
    def _draw_summary(self):
        pygame.draw.line(self.screen, (60, 60, 80), (60, 372), (940, 372), 1)
        s = self.stats
        total = s.get("total", 0)
        wins = s.get("wins", 0)
        losses = s.get("losses", 0)
        best = s.get("best_wpm", 0)
        avg  = s.get("avg_wpm", 0)
        rate  = round((wins / total) * 100) if total > 0 else 0
        label = self.font_header.render("LIFETIME STATS", True, (120, 120, 120))
        self.screen.blit(label, (65, 378))
        summary_items = [
            f"Races: {total}",
            f"Wins: {wins}",
            f"Losses: {losses}",
            f"Win Rate: {rate}%",
            f"Best WPM: {best}",
            f"Avg WPM: {avg}",
        ]
        x = 65
        for item in summary_items:
            s_surf = self.font_stat.render(item, True, (200, 200, 200))
            self.screen.blit(s_surf, (x, 398))
            x += s_surf.get_width() + 28
    def _draw_hints(self):
        hints = "↑↓ select   DEL delete   D filter diff   R filter result   S sort   ESC back"
        h = self.font_small.render(hints, True, (70, 70, 70))
        self.screen.blit(h, h.get_rect(center=(500, 578)))
    def _draw_confirm_overlay(self):
        overlay = pygame.Surface((1000, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        box = pygame.Rect(300, 220, 400, 140)
        pygame.draw.rect(self.screen, (25, 25, 40), box, border_radius=10)
        pygame.draw.rect(self.screen, (220, 60, 60), box, 2, border_radius=10)
        msg = self.font_row.render("Delete this score?", True, (255, 255, 255))
        hint = self.font_small.render("Y confirm  N / ESC  cancel", True, (180, 180, 180))
        self.screen.blit(msg,  msg.get_rect(center=(500, 265)))
        self.screen.blit(hint, hint.get_rect(center=(500, 310)))