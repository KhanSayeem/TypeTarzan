import time
class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.user_input = ""
        self.wpm = 0
        self.typing_start_time = None
        self.last_typed_time = None
        self.idle_threshold = 1.5
        self.decay_rate = 0.98
    def handle_keypress(self, event, target_text):
        import pygame
        if event.type == pygame.TEXTINPUT:
            if len(self.user_input) < len(target_text):
                if self.typing_start_time is None:
                    self.typing_start_time = time.time()
                self.user_input += event.text
                self.last_typed_time = time.time()
                self.wpm = self._calculate_wpm()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
                self.last_typed_time = time.time()

    def apply_idle_decay(self):
        if self.last_typed_time is not None:
            idle_time = time.time() - self.last_typed_time
            if idle_time > self.idle_threshold:
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
    def _calculate_wpm(self):
        if self.typing_start_time is None:
            return 0
        if len(self.user_input) < 5:
            return 0
        elapsed_mins = (time.time() - self.typing_start_time) / 60
        if elapsed_mins == 0:
            return 0
        return (len(self.user_input) / 5) / elapsed_mins
    def reset(self):
        self.user_input = ""
        self.wpm = 0
        self.typing_start_time = None
        self.last_typed_time = None