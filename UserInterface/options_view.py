import arcade

from arcade.gui import UIFlatButton, UIManager, UIAnchorLayout, UILabel, UIBoxLayout, UIInputText, UIGridLayout
from docutils.parsers.rst.directives.misc import Title

from Database.models import User
from Database.session import Session
from UserInterface import main_menu
from UserInterface.view_utils import BaseView


class Options(BaseView):
    def __init__(self):
        super().__init__()
        self.back_view=self.window.main_view
        self.anchor = self.manager.add(UIAnchorLayout())
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(text="Ustawienia", width=1000, text_color=arcade.color.BLACK, font_size=100,
                             font_name="Arial")
        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )





