class TextManager:
    PRESET_TEXTS = {
        "easy": [
            "the cat sat on the mat",
            "dogs run and jump and play",
            "she sells sea shells by the sea shore",
        ],
        "medium": [
            "the quick brown fox jumps over the lazy dog near the riverbank",
            "typing fast requires focus and consistent daily practice to improve",
            "python is a powerful language used in games web and data science",
        ],
        "hard": [
            "as the storm approached the coastal town residents scrambled to secure their belongings and evacuate to higher ground",
            "the scientist carefully documented each variable in the experiment ensuring that no detail however small was overlooked or forgotten",
            "competitive typing requires not only speed but also exceptional accuracy under pressure and the ability to maintain focus for extended periods",
        ]
    }
    def __init__(self):
        self.custom_text = None
        self.selected_text = None
        self.difficulty = None
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.selected_text = None
        self.custom_text = None
    def get_presets(self):
        if self.difficulty is None: return []
        return self.PRESET_TEXTS[self.difficulty]
    def select_preset(self, index):
        presets = self.get_presets()
        if 0 <= index < len(presets):
            self.selected_text = presets[index]
    def set_custom(self, text):
        text = text.strip()
        if len(text) < 10:
            return False, "Text must be at least 10 characters."
        if not text.isprintable():
            return False, "Text contains invalid characters."
        self.custom_text = text
        self.selected_text = text
        return True, "OK"
    def get_text(self): return self.selected_text
    def is_ready(self): return self.selected_text is not None