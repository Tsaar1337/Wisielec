import arcade

from Database import init_db
from UserInterface import *
from UserInterface.scoreboard_view import ScoreboardView


class HangmanGame(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, "Hangman")
        self.login_view = LoginView()
        self.main_view = MainMenu()
        self.register_view=RegisterView()
        self.options_view=Options()
        self.menu_game_view = MenuGameView()
        self.game_view = GameView()
        self.info_view = InfoView()
        self.scoreboard_view = ScoreboardView()
        self.show_view(self.login_view)



if __name__ == "__main__":
    init_db()
    game = HangmanGame()
    arcade.run()


