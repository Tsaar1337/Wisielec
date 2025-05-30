import arcade
from arcade.gui import UIAnchorLayout, UILabel, UIBoxLayout

from UserInterface.view_utils import BaseView


class InfoView(BaseView):

    def __init__(self):
        super().__init__()
        self.back_view = self.window.menu_game_view
        font = "Comic sans MS"
        self.anchor = self.manager.add(UIAnchorLayout())
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(text="Informacje o grze", width=1000, text_color=arcade.color.BLACK, font_size=100,
                             font_name=font)
        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )
