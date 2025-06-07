import arcade
from arcade.gui import UIBoxLayout, UILabel

from UserInterface.view_utils import BaseView


class TwoPlayerGameView(BaseView):
    def __init__(self, back_view):
        super().__init__(back_view)
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(text="Tryb dwóch gracz", width=1000, text_color=arcade.color.BLACK, font_size=100, font_name=self.font)
        temp_label = UILabel(text="W kolejnej aktualizacji", text_color=arcade.color.RED, font_size=70, font_name=self.font)

        title_box.add(main_label)
        title_box.add(temp_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )