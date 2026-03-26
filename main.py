import pygame
from sys import exit
from src.screens.welcome_screen import WelcomeScreen
from src.screens.main_menu import MainMenu
from src.screens.difficulty_screen import DifficultyScreen
from src.screens.text_select_screen import TextSelectScreen
from src.screens.game_screen import GameScreen
from src.screens.result_screen import ResultScreen
from src.screens.high_scores_screen import HighScoresScreen
from src.screens.exit_screen import ExitScreen
from src.text_manager import TextManager
from src.storage import Storage
pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("TypeTarzan")
clock = pygame.time.Clock()
text_manager = TextManager()
storage = Storage()
game_screen = GameScreen(screen, clock, text_manager, storage)
result_screen = ResultScreen(screen, clock, storage, text_manager)
screens = {
    "welcome":WelcomeScreen(screen, clock),
    "menu": MainMenu(screen, clock),
    "difficulty": DifficultyScreen(screen, clock, text_manager),
    "textselect": TextSelectScreen(screen, clock, text_manager),
    "game": game_screen,
    "result":result_screen,
    "highscores": HighScoresScreen(screen, clock, storage),
    "exit":ExitScreen(screen, clock, storage),
}
current_screen = screens["welcome"]
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    current_screen.handle_events(events)
    current_screen.update()
    current_screen.draw()
    if current_screen.next_screen is not None:
        next_name = current_screen.next_screen
        current_screen.next_screen = None
        if next_name in screens:
            next_screen = screens[next_name]
            if next_name == "result":
                next_screen.on_enter(game_screen.engine, game_screen.player)
            elif hasattr(next_screen, "on_enter"):
                next_screen.on_enter()
            current_screen = next_screen
    pygame.display.update()
    clock.tick(60)