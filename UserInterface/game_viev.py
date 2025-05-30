import arcade
from arcade.gui import UIFlatButton, UIManager, UIAnchorLayout, UILabel, UIBoxLayout, UIInputText, UIGridLayout

from UserInterface.view_utils import BaseView


class GameView(BaseView):

    def __init__(self):
        super().__init__()
        font = "Comic sans MS"
        self.back_view = self.window.menu_game_view
        self.anchor = self.manager.add(UIAnchorLayout())
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(text="Tu będzie gra", width=1000, text_color=arcade.color.BLACK, font_size=100,
                             font_name=font)
        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )



