import arcade
from arcade.gui import UIBoxLayout, UILabel
from UserInterface.view_utils import BaseView


class TwoPlayerGameView(BaseView):
    """Widok trybu gry dla dwóch graczy.

    Klasa odpowiedzialna za wyświetlanie interfejsu użytkownika w trybie gry wieloosobowej.
    Dziedziczy po klasie BaseView i tworzy podstawowy układ UI z tytułem i informacją o statusie.

    Args:
        back_view: Widok, do którego nastąpi powrót po opuszczeniu obecnego widoku.

    Attributes:
        anchor: Główny kontener dla elementów UI.
    """

    def __init__(self, back_view):
        """Inicjalizuje widok gry dla dwóch graczy.

        Tworzy i konfiguruje podstawowe elementy interfejsu użytkownika, w tym:
        - Box layout do organizacji elementów w pionie
        - Etykietę z tytułem trybu gry
        - Etykietę informującą o statusie implementacji

        Args:
            back_view: Referencja do poprzedniego widoku.
        """
        super().__init__(back_view)
        # Utworzenie głównego kontenera dla elementów UI
        title_box = UIBoxLayout(vertical=True, space_between=20)
        
        # Utworzenie głównej etykiety z tytułem
        main_label = UILabel(
            text="Tryb dwóch gracz", 
            width=1000, 
            text_color=arcade.color.BLACK, 
            font_size=100, 
            font_name=self.font
        )
        
        # Utworzenie etykiety informacyjnej
        temp_label = UILabel(
            text="W kolejnej aktualizacji", 
            text_color=arcade.color.RED, 
            font_size=70, 
            font_name=self.font
        )

        # Dodanie etykiet do kontenera
        title_box.add(main_label)
        title_box.add(temp_label)
        
        # Konfiguracja pozycjonowania kontenera w widoku
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )