import time
from collections import deque
class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.user_input = ""
        self.wpm = 0
        self.typing_start_time = None
        self.last_typed_time = None
        self.keypress_log = deque()
        self.window_sec = 3
        self.idle_threshold = 1.5
        self.decay_rate = 0.97
    def handle_keypress(self, event, target_text):
        import pygame
        if event.type == pygame.TEXTINPUT:
            if len(self.user_input) < len(target_text):
                if self.typing_start_time is None:
                    self.typing_start_time = time.time()
                self.user_input += event.text
                self.last_typed_time = time.time()
                self._log_keypress(target_text)
                self.wpm = self._calculate_wpm()

        elif event.type == pygame.KEYDOWN:
            import pygame
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
                self.last_typed_time = time.time()

    def _log_keypress(self, target_text):
        """Log a keypress only if the character typed was correct."""
        i = len(self.user_input) - 1
        if i >= 0 and i < len(target_text):
            if self.user_input[i] == target_text[i]:
                self.keypress_log.append(time.time())

    def _calculate_wpm(self):
        now = time.time()
        cutoff = now - self.window_sec
        while self.keypress_log and self.keypress_log[0] < cutoff:
            self.keypress_log.popleft()
        correct_chars_in_window = len(self.keypress_log)
        if correct_chars_in_window == 0:
            return 0
        wpm = (correct_chars_in_window / 5) * (60 / self.window_sec)
        return wpm
    def apply_idle_decay(self):
        if self.last_typed_time is not None:
            idle = time.time() - self.last_typed_time
            if idle > self.idle_threshold:
                self.wpm *= self.decay_rate
    def get_speed(self):
        return self.wpm / 10
    def is_finished(self, target_text):
        return self.user_input == target_text
    def get_accuracy(self, target_text):
        if not self.user_input:
            return 0
        correct = sum(
            1 for i, ch in enumerate(self.user_input)
            if i < len(target_text) and ch == target_text[i]
        )
        return round((correct / len(self.user_input)) * 100)
    def reset(self):
        self.user_input = ""
        self.wpm = 0
        self.typing_start_time = None
        self.last_typed_time = None
        self.keypress_log = deque()