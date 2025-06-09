"""
Moduł implementujący główne menu gry Wisielec.
Zapewnia dostęp do wszystkich głównych funkcji aplikacji poprzez intuicyjny interfejs użytkownika.
"""

import arcade
from arcade.gui import UIFlatButton, UILabel, UIBoxLayout, UIGridLayout
from UserInterface.view_utils import BaseView


class MainMenu(BaseView):
    """Główne menu gry Wisielec.

    Klasa implementuje główny ekran menu gry, zawierający:
    - Tytuł gry
    - Przyciski nawigacyjne do różnych sekcji
    - Informację o zalogowanym użytkowniku

    Attributes:
        user_label (UILabel): Etykieta wyświetlająca nazwę zalogowanego użytkownika.
    """

    def __init__(self):
        """Inicjalizuje główne menu gry.

        Tworzy kompletny interfejs użytkownika zawierający wszystkie
        elementy menu głównego i konfiguruje ich zachowanie.
        """
        super().__init__()
        self._setup_title()
        self._setup_navigation_buttons()
        self._setup_user_info()

    def _setup_title(self):
        """Konfiguruje sekcję tytułową menu.

        Tworzy i pozycjonuje tytuł gry "Wisielec" w górnej części ekranu.
        """
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(
            text="Wisielec",
            width=1000,
            text_color=arcade.color.BLACK,
            font_size=100,
            font_name=self.font
        )
        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )

    def _setup_navigation_buttons(self):
        """Konfiguruje przyciski nawigacyjne menu.

        Tworzy i konfiguruje:
        - Przycisk rozpoczęcia gry
        - Przycisk ustawień
        - Przycisk tablicy wyników
        - Przycisk wylogowania
        """
        # Tworzenie przycisków
        buttons = self._create_navigation_buttons()
        
        # Konfiguracja obsługi zdarzeń
        self._setup_button_handlers(*buttons)
        
        # Tworzenie układu przycisków
        self._setup_button_layout(*buttons)

    def _create_navigation_buttons(self):
        """Tworzy przyciski nawigacyjne.

        Returns:
            tuple: Krotka zawierająca utworzone przyciski (play, options, scoreboard, logout).
        """
        play_button = UIFlatButton(text="Graj", width=350)
        options_button = UIFlatButton(text="Ustawienia", width=167.5)
        scoreboard_button = UIFlatButton(text="Wyniki", width=167.5)
        logout_button = UIFlatButton(text="Wyloguj", width=350)
        
        return play_button, options_button, scoreboard_button, logout_button

    def _setup_button_handlers(self, play_button, options_button, 
                             scoreboard_button, logout_button):
        """Konfiguruje obsługę zdarzeń dla przycisków.

        Args:
            play_button (UIFlatButton): Przycisk rozpoczęcia gry.
            options_button (UIFlatButton): Przycisk ustawień.
            scoreboard_button (UIFlatButton): Przycisk tablicy wyników.
            logout_button (UIFlatButton): Przycisk wylogowania.
        """
        @play_button.event("on_click")
        def on_click_play_button(event):
            """Przechodzi do menu wyboru trybu gry."""
            self.window.show_view(self.window.menu_game_view)

        @options_button.event("on_click")
        def on_click_options_button(event):
            """Przechodzi do widoku ustawień."""
            self.window.show_view(self.window.options_view)

        @scoreboard_button.event("on_click")
        def on_click_scoreboard_button(event):
            """Przechodzi do widoku tablicy wyników."""
            self.window.show_view(self.window.scoreboard_view)

        @logout_button.event("on_click")
        def on_click_exit_button(event):
            """Wylogowuje użytkownika i wraca do ekranu logowania."""
            self.window.show_view(self.window.login_view)

    def _setup_button_layout(self, play_button, options_button,
                           scoreboard_button, logout_button):
        """Konfiguruje układ przycisków w interfejsie.

        Args:
            play_button (UIFlatButton): Przycisk rozpoczęcia gry.
            options_button (UIFlatButton): Przycisk ustawień.
            scoreboard_button (UIFlatButton): Przycisk tablicy wyników.
            logout_button (UIFlatButton): Przycisk wylogowania.
        """
        buttons_box = UIBoxLayout(vertical=True, space_between=15)

        # Utworzenie siatki dla przycisków ustawień i wyników
        grid_layout = UIGridLayout(
            column_count=2,
            row_count=1,
            horizontal_spacing=15
        )
        grid_layout.add(column=0, row=0, child=options_button)
        grid_layout.add(column=1, row=0, child=scoreboard_button)

        # Dodanie wszystkich elementów do głównego kontenera
        buttons_box.add(play_button)
        buttons_box.add(grid_layout)
        buttons_box.add(logout_button)
        
        # Pozycjonowanie kontenera przycisków
        self.anchor.add(
            child=buttons_box,
            anchor_x="center",
            anchor_y="center",
            align_y=-60
        )

    def _setup_user_info(self):
        """Konfiguruje wyświetlanie informacji o zalogowanym użytkowniku.

        Tworzy i pozycjonuje etykietę pokazującą nazwę zalogowanego użytkownika
        w prawym dolnym rogu ekranu.
        """
        current_user = "Gosc"  # Domyślna wartość
        
        self.user_label = UILabel(
            text=f"Zalogowany: {current_user}",
            font_size=14,
            text_color=arcade.color.DARK_GRAY,
            width=200,
            align="right"
        )

        self.anchor.add(
            child=self.user_label,
            anchor_x="right",
            anchor_y="bottom",
            align_x=-20,
            align_y=20
        )