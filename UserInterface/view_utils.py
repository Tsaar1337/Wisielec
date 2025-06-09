"""
Moduł zawierający podstawowe komponenty interfejsu użytkownika i narzędzia pomocnicze.

Moduł dostarcza:
- Funkcje do obsługi komunikatów o błędach
- Podstawową klasę widoku z wspólną funkcjonalnością
- Specjalistyczny komponent do wprowadzania haseł
"""

from functools import partial
import arcade
from arcade.gui import UILabel, UIInputText, UIAnchorLayout


def clear_error_label(delta_time: float, text_label: UILabel) -> None:
    """Czyści tekst z etykiety błędu.

    Args:
        delta_time (float): Czas, który upłynął od ostatniej aktualizacji (wymagany przez arcade).
        text_label (UILabel): Etykieta, której tekst ma zostać wyczyszczony.
    """
    text_label.text = ""


def schedule_clear_error_label(text_label: UILabel, delay: float = 2.0) -> None:
    """Planuje wyczyszczenie etykiety błędu po określonym czasie.

    Args:
        text_label (UILabel): Etykieta do wyczyszczenia.
        delay (float, optional): Opóźnienie w sekundach przed wyczyszczeniem. Domyślnie 2.0.
    """
    arcade.schedule(partial(clear_error_label, text_label=text_label), delay)


class BaseView(arcade.View):
    """Podstawowa klasa widoku implementująca wspólne funkcjonalności.

    Zapewnia podstawową strukturę dla wszystkich widoków w aplikacji, w tym:
    - Zarządzanie UI
    - Obsługę powrotu do poprzedniego widoku
    - Wspólne ustawienia wyglądu

    Args:
        back_view (arcade.View, optional): Widok, do którego nastąpi powrót po naciśnięciu ESC.
            Domyślnie None.

    Attributes:
        manager (arcade.gui.UIManager): Zarządca interfejsu użytkownika.
        anchor (UIAnchorLayout): Główny kontener dla elementów UI.
        back_view (arcade.View): Referencja do poprzedniego widoku.
        font (str): Domyślna czcionka używana w widoku.
    """

    def __init__(self, back_view=None):
        """Inicjalizuje podstawowy widok.

        Args:
            back_view (arcade.View, optional): Widok, do którego nastąpi powrót.
                Domyślnie None.
        """
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.anchor = self.manager.add(UIAnchorLayout())
        self.back_view = back_view
        self.font = "Comic sans MS"

    def on_show_view(self):
        """Wywoływane gdy widok jest pokazywany.

        Ustawia kolor tła i aktywuje menedżera UI.
        """
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.manager.enable()

    def on_draw(self):
        """Wywoływane przy każdym odświeżeniu ekranu.

        Czyści ekran i rysuje elementy interfejsu użytkownika.
        """
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        """Wywoływane gdy widok jest ukrywany.

        Dezaktywuje menedżera UI.
        """
        self.manager.disable()

    def on_key_press(self, key, modifiers):
        """Obsługuje zdarzenia naciśnięcia klawiszy.

        Implementuje funkcjonalność powrotu do poprzedniego widoku
        po naciśnięciu klawisza ESC.

        Args:
            key: Kod naciśniętego klawisza.
            modifiers: Modyfikatory klawiatury (np. Shift, Ctrl).
        """
        if key == arcade.key.ESCAPE and self.back_view:
            self.window.show_view(self.back_view)


class PasswordInput(UIInputText):
    """Specjalistyczny komponent do wprowadzania haseł.

    Rozszerza standardowe pole tekstowe, dodając funkcjonalność maskowania
    wprowadzanego tekstu gwiazdkami (*) przy jednoczesnym zachowaniu
    rzeczywistej wartości hasła.

    Attributes:
        real_text (str): Przechowuje rzeczywisty tekst hasła.
    """

    def __init__(self, **kwargs):
        """Inicjalizuje pole wprowadzania hasła.

        Args:
            **kwargs: Parametry przekazywane do konstruktora UIInputText.
        """
        super().__init__(**kwargs)
        self.real_text = ""

    def on_event(self, event):
        """Obsługuje zdarzenia związane z wprowadzaniem tekstu.

        Przechwytuje wprowadzany tekst, aktualizuje rzeczywistą wartość
        hasła i wyświetla odpowiednią liczbę gwiazdek.

        Args:
            event: Zdarzenie wprowadzania tekstu.

        Returns:
            bool: Flaga wskazująca czy zdarzenie zostało obsłużone.
        """
        handled = super().on_event(event)

        # Aktualizacja rzeczywistego tekstu na podstawie zmian w polu
        if len(self.text) > len(self.real_text):
            add_char = self.text[len(self.real_text)]
            self.real_text += add_char
        elif len(self.text) < len(self.real_text):
            self.real_text = self.real_text[:len(self.text)]

        # Zastąpienie tekstu gwiazdkami
        self.text = "*" * len(self.real_text)

        return handled

    def get_real_text(self) -> str:
        """Zwraca rzeczywisty tekst hasła.

        Returns:
            str: Niezamaskowany tekst hasła.
        """
        return self.real_text