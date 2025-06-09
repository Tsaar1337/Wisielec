"""
Moduł zawierający widok opcji aplikacji, umożliwiający konfigurację ustawień,
takich jak głośność dźwięku.
"""

import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UISlider
from UserInterface.view_utils import BaseView


class Options(BaseView):
    """Widok opcji aplikacji umożliwiający konfigurację ustawień.

    Klasa implementuje interfejs użytkownika do zarządzania ustawieniami aplikacji,
    w tym kontrolę głośności dźwięku. Zapewnia interaktywny suwak do regulacji
    głośności oraz wizualną reprezentację aktualnego poziomu głośności.

    Args:
        back_view (arcade.View): Widok, do którego nastąpi powrót po wyjściu z opcji.

    Attributes:
        volume_label (UILabel): Etykieta wyświetlająca aktualny poziom głośności.
        volume_slider (UISlider): Suwak do regulacji poziomu głośności.
    """

    def __init__(self, back_view):
        """Inicjalizuje widok opcji.

        Tworzy interfejs użytkownika zawierający:
        - Tytuł widoku
        - Sekcję kontroli głośności z etykietą i suwakiem

        Args:
            back_view (arcade.View): Widok, do którego nastąpi powrót.
        """
        super().__init__(back_view)

        self._setup_title()
        self._setup_volume_controls()

    def _setup_title(self):
        """Konfiguruje sekcję tytułową widoku.

        Tworzy i pozycjonuje tytuł "Ustawienia" w górnej części ekranu.
        """
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(
            text="Ustawienia",
            font_size=60,
            text_color=arcade.color.BLACK,
            width=600,
            font_name=self.font
        )

        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )

    def _setup_volume_controls(self):
        """Konfiguruje elementy kontroli głośności.

        Tworzy i pozycjonuje:
        - Etykietę wyświetlającą aktualny poziom głośności
        - Suwak do regulacji głośności
        """
        volume_box = UIBoxLayout(vertical=True, space_between=20)

        # Konfiguracja etykiety głośności
        self.volume_label = UILabel(
            text=f"Głośność: {int(self.window.volume * 100)}%",
            font_size=30,
            text_color=arcade.color.BLACK
        )
        volume_box.add(self.volume_label)

        # Konfiguracja suwaka głośności
        self.volume_slider = UISlider(
            value=self.window.volume,
            min_value=0.0,
            max_value=1.0,
            width=300,
            step=0.01
        )
        self.volume_slider.on_change = self.on_volume_change
        volume_box.add(self.volume_slider)

        # Pozycjonowanie kontrolek głośności
        self.anchor.add(
            child=volume_box,
            anchor_x="center",
            anchor_y="center",
            align_y=-50
        )

    def on_volume_change(self, event):
        """Obsługuje zdarzenie zmiany poziomu głośności.

        Aktualizuje głośność w aplikacji i odświeża wyświetlany poziom
        głośności w interfejsie użytkownika.

        Args:
            event: Zdarzenie zmiany wartości suwaka (niewykorzystywane).
        """
        new_volume = self.volume_slider.value
        self.window.volume = new_volume
        self.update_volume_label()
        self.set_music_volume(new_volume)

    def update_volume_label(self):
        """Aktualizuje tekst etykiety wyświetlającej poziom głośności.

        Konwertuje wartość głośności na procenty i wyświetla ją w etykiecie.
        """
        self.volume_label.text = f"Głośność: {int(self.window.volume * 100)}%"

    def set_music_volume(self, volume: float):
        """Ustawia nowy poziom głośności dla odtwarzacza muzyki.

        Próbuje zmienić głośność "na żywo". Jeśli to nie jest możliwe,
        zatrzymuje i ponownie uruchamia odtwarzacz muzyki z nową głośnością.

        Args:
            volume (float): Nowy poziom głośności w zakresie 0.0-1.0.
        """
        if self.window.music_player:
            try:
                # Próba zmiany głośności bez przerywania odtwarzania
                self.window.music_player.volume = volume
            except AttributeError:
                # Restart odtwarzacza z nową głośnością w przypadku błędu
                self.window.music_player.pause()
                self.window.music_player = self.window.background_music.play(
                    volume=volume,
                    loop=True
                )