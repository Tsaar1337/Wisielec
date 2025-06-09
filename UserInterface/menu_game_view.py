"""
Moduł zawierający widok menu wyboru trybu gry, umożliwiający wybór różnych
wariantów rozgrywki oraz dostęp do informacji o grze.
"""

import arcade
from arcade.gui import (
    UIFlatButton, UIManager, UIAnchorLayout, UILabel,
    UIBoxLayout, UIInputText, UIGridLayout
)
from docutils.nodes import title
from .game_view import GameView
from UserInterface.view_utils import schedule_clear_error_label, BaseView


class MenuGameView(BaseView):
    """Widok menu wyboru trybu gry.

    Klasa implementuje interfejs użytkownika umożliwiający wybór różnych
    trybów rozgrywki, w tym:
    - Grę na czas
    - Grę na życia
    - Grę przeciwko innemu graczowi
    Dodatkowo zapewnia dostęp do informacji o grze.

    Args:
        back_view (arcade.View): Widok, do którego nastąpi powrót.

    Attributes:
        anchor (UIAnchorLayout): Główny kontener dla elementów UI.
    """

    def __init__(self, back_view):
        """Inicjalizuje widok menu wyboru trybu gry.

        Tworzy interfejs użytkownika zawierający:
        - Tytuł menu
        - Przyciski wyboru trybu gry
        - Przycisk informacji
        - Etykietę błędów

        Args:
            back_view (arcade.View): Widok, do którego nastąpi powrót.
        """
        super().__init__(back_view)
        
        self._setup_title()
        self._setup_menu_buttons()

    def _setup_title(self):
        """Konfiguruje sekcję tytułową widoku.

        Tworzy i pozycjonuje tytuł "Wybierz tryb gry" w górnej części ekranu.
        """
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(
            text="Wybierz tryb gry",
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

    def _setup_menu_buttons(self):
        """Konfiguruje przyciski menu i ich funkcjonalności.

        Tworzy i konfiguruje:
        - Przycisk trybu gry na czas
        - Przycisk trybu gry na życia
        - Przycisk gry przeciwko innemu graczowi
        - Przycisk informacji
        - Etykietę błędów
        """
        # Utworzenie przycisków
        play_time_button = UIFlatButton(text="Na Czas", width=200)
        play_oponent_button = UIFlatButton(text="Przeciwko sobie", width=200)
        play_health_button = UIFlatButton(text="Na życia", width=200)
        info_button = UIFlatButton(text="Informacje", width=200)
        error_label = UILabel(text=" ", text_color=arcade.color.RED, font_size=12)

        # Konfiguracja obsługi zdarzeń dla przycisków
        self._setup_button_handlers(
            play_time_button,
            play_health_button,
            play_oponent_button,
            info_button
        )

        # Utworzenie i konfiguracja układu przycisków
        self._setup_button_layout(
            play_time_button,
            play_health_button,
            play_oponent_button,
            info_button,
            error_label
        )

    def _setup_button_handlers(self, play_time_button, play_health_button,
                             play_oponent_button, info_button):
        """Konfiguruje obsługę zdarzeń dla przycisków menu.

        Args:
            play_time_button (UIFlatButton): Przycisk trybu gry na czas.
            play_health_button (UIFlatButton): Przycisk trybu gry na życia.
            play_oponent_button (UIFlatButton): Przycisk gry przeciwko innemu graczowi.
            info_button (UIFlatButton): Przycisk informacji.
        """
        @play_time_button.event("on_click")
        def on_click_play_time(event):
            """Obsługuje rozpoczęcie gry w trybie na czas."""
            self.window.game_view.time_mode = True
            self.window.show_view(self.window.game_view_on_time)

        @play_health_button.event("on_click")
        def on_click_play_health(event):
            """Obsługuje rozpoczęcie gry w trybie na życia."""
            self.window.game_view.time_mode = False
            self.window.show_view(self.window.game_view)

        @play_oponent_button.event("on_click")
        def on_click_play_opponent(event):
            """Obsługuje rozpoczęcie gry przeciwko innemu graczowi."""
            self.window.show_view(self.window.two_player_game_view)

        @info_button.event("on_click")
        def on_click_info(event):
            """Obsługuje wyświetlenie informacji o grze."""
            self.window.show_view(self.window.info_view)

    def _setup_button_layout(self, play_time_button, play_health_button,
                           play_oponent_button, info_button, error_label):
        """Konfiguruje układ przycisków w interfejsie.

        Args:
            play_time_button (UIFlatButton): Przycisk trybu gry na czas.
            play_health_button (UIFlatButton): Przycisk trybu gry na życia.
            play_oponent_button (UIFlatButton): Przycisk gry przeciwko innemu graczowi.
            info_button (UIFlatButton): Przycisk informacji.
            error_label (UILabel): Etykieta do wyświetlania błędów.
        """
        main_box = UIBoxLayout(vertical=True, space_between=20)
        grid_layout = UIGridLayout(
            column_count=2,
            row_count=3,
            horizontal_spacing=20,
            vertical_spacing=10
        )

        # Dodanie przycisków do siatki
        grid_layout.add(column=0, row=0, child=play_time_button)
        grid_layout.add(column=1, row=0, child=play_health_button)
        grid_layout.add(column=0, row=1, child=play_oponent_button)
        grid_layout.add(column=1, row=1, child=info_button)

        # Konfiguracja głównego kontenera
        main_box.add(grid_layout)
        main_box.add(error_label)
        self.anchor.add(child=main_box)