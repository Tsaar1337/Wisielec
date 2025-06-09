"""
Główny moduł gry Wisielec (Hangman).

Ten moduł zawiera główną klasę gry oraz punkt wejściowy aplikacji.
Inicjalizuje okno gry, zarządza widokami i obsługuje podstawowe
funkcjonalności jak muzyka w tle.

Dependencies:
    - arcade: Biblioteka do tworzenia gier 2D
    - Database: Moduł obsługi bazy danych
    - UserInterface: Moduł zawierający wszystkie widoki gry
"""

import arcade

from Database import init_db
from Database.database_logic import load_words_from_json
from UserInterface import *
from UserInterface.game_view import GameViewOnTime

from UserInterface.scoreboard_view import ScoreboardView
from UserInterface.two_player_game_view import TwoPlayerGameView


class HangmanGame(arcade.Window):
    """
      Główna klasa gry dziedzicząca po arcade.Window.

      Zarządza głównym oknem gry, wszystkimi widokami oraz muzyką w tle.

      Attributes:
          user_one: Pierwszy gracz
          user_two: Drugi gracz (w trybie dwuosobowym)
          background_music: Ścieżka dźwiękowa gry
          volume (float): Głośność muzyki (0.0 - 1.0)
          music_player: Obiekt odtwarzacza muzyki

      Views:
          login_view: Widok logowania
          register_view: Widok rejestracji
          main_view: Widok menu głównego
          options_view: Widok opcji
          menu_game_view: Widok menu gry
          game_view: Widok pojedynczej gry
          game_view_on_time: Widok gry na czas
          scoreboard_view: Widok tablicy wyników
          info_view: Widok informacji
          two_player_game_view: Widok gry dwuosobowej
      """

    def __init__(self):
        """
              Inicjalizuje okno gry i wszystkie jego komponenty.

              - Tworzy okno o wymiarach 1280x720 pikseli
              - Ładuje i rozpoczyna odtwarzanie muzyki w tle
              - Inicjalizuje wszystkie widoki gry
              """

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
        self.two_player_game_view = TwoPlayerGameView(self.menu_game_view)



        self.show_view(self.info_view )

        def on_close(self):
            """
                  Obsługuje zamknięcie okna gry.

                  - Zatrzymuje odtwarzanie muzyki w tle
                  - Wykonuje standardową procedurę zamknięcia okna
                  """

            # Zatrzymaj muzykę przy zamknięciu gry
            if self.music_player:
                self.music_player.pause()
            super().on_close()


if __name__ == "__main__":
    init_db()
    load_words_from_json("Database/words.json")
    game = HangmanGame()
    arcade.run()


