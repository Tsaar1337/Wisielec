import arcade
from sqlalchemy.sql.operators import truediv

from Database import init_db, User
from Logic.database_logic import load_words_from_json
from UserInterface import *
from UserInterface.game_view import GameViewOnTime

from UserInterface.scoreboard_view import ScoreboardView


class HangmanGame(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, "Hangman")
        self.user_one = None
        self.user_two = None
        self.background_music = arcade.load_sound("Sounds/MuzykaGra.mp3")
        self.volume = 0.1
        self.music_player = self.background_music.play(self.volume, loop=True)
        self.login_view = LoginView()
        self.register_view=RegisterView(self.login_view)
        self.main_view = MainMenu()
        self.options_view=Options(self.main_view)
        self.menu_game_view = MenuGameView(self.main_view)
        self.game_view = GameView(self.menu_game_view, True)
        self.game_view_on_time = GameViewOnTime(self.menu_game_view, True)
        self.scoreboard_view = ScoreboardView(self.main_view)
        self.info_view = InfoView(self.menu_game_view)



        self.show_view(self.login_view)

        def on_close(self):
            # Zatrzymaj muzykę przy zamknięciu gry
            if self.music_player:
                self.music_player.pause()
            super().on_close()


if __name__ == "__main__":
    init_db()
    load_words_from_json("words.json")
    game = HangmanGame()
    arcade.run()


