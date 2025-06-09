import arcade
from arcade.gui import UIAnchorLayout, UILabel, UIBoxLayout

from UserInterface.view_utils import BaseView


class InfoView(BaseView):

    def __init__(self, back_view):
        super().__init__(back_view)
        self.back_view = self.window.menu_game_view
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(text="Informacje o grze", width=1000, text_color=arcade.color.BLACK, font_size=100,
                             font_name=self.font)
        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )
        # Opis gry
        description_label = UILabel(
            text="WISIELEC – klasyczna gra słowna w nowoczesnym wydaniu!\n"
                 "Zgaduj litery i odgadnij hasło zanim skończy się czas, życie lub pokona Cię przeciwnik.",
            width=800,
            text_color=arcade.color.DARK_BLUE,
            font_size=20,
            font_name=self.font,
            multiline=True
        )
        title_box.add(description_label)

        # Tryby gry
        modes_label = UILabel(
            text="Tryby gry:\n"
                 "1. Na czas – odgadnij hasło zanim upłynie limit czasu(60 sekund).\n"
                 "2. Na życie – masz ograniczoną liczbę błędów(6), każda pomyłka zbliża Cię do porażki.\n"
                 "3. Przeciwko sobie – dostępne w najstępnej aktualizacji 11.06.2025",
            width=800,
            text_color=arcade.color.DARK_GREEN,
            font_size=20,
            font_name=self.font,
            multiline=True
        )
        title_box.add(modes_label)
