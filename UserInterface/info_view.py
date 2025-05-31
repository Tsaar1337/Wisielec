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
