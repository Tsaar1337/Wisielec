import arcade

from arcade.gui import UIFlatButton, UIManager, UIAnchorLayout, UILabel, UIBoxLayout, UIInputText, UIGridLayout
from docutils.parsers.rst.directives.misc import Title

from Database.models import User
from Database.session import Session
from UserInterface.view_utils import BaseView


class MainMenu(BaseView):
    def __init__(self):
        super().__init__()
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(text="Wisielec", width=1000, text_color=arcade.color.BLACK, font_size=100, font_name=self.font)
        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )

        play_button = UIFlatButton(text="Graj", width=350)
        options_button = UIFlatButton(text="Ustawienia", width=167.5)
        scoreboard_button = UIFlatButton(text="Wyniki", width=167.5)
        logout_button = UIFlatButton(text="Wyloguj", width=350)

        @play_button.event("on_click")
        def on_click_play_button(event):
            self.window.show_view(self.window.menu_game_view)

        @options_button.event("on_click")
        def on_click_options_button(event):
            self.window.show_view(self.window.options_view)

        @scoreboard_button.event("on_click")
        def on_click_scoreboard_button(event):
            self.window.show_view(self.window.scoreboard_view)

        @logout_button.event("on_click")
        def on_click_exit_button(event):
            self.window.show_view(self.window.login_view)

        buttons_box = UIBoxLayout(vertical=True, space_between=15)

        grid_layout = UIGridLayout(column_count=2, row_count=1, horizontal_spacing=15)
        grid_layout.add(column=0, row=0, child=options_button)
        grid_layout.add(column=1, row=0, child=scoreboard_button)

        buttons_box.add(play_button)
        buttons_box.add(grid_layout)
        buttons_box.add(logout_button)
        self.anchor.add(
            child=buttons_box,
            anchor_x="center",
            anchor_y="center",
            align_y=-60
        )
        current_user = getattr(self.window, "current_user", "Gość")


        user_label = UILabel(
            text=f"Zalogowany: {current_user}",
            font_size=14,
            text_color=arcade.color.DARK_GRAY,
            width=200,
            align="right"
        )

        self.anchor.add(
            child=user_label,
            anchor_x="right",
            anchor_y="bottom",
            align_x=-20,  # odsunięcie od prawej krawędzi
            align_y=20  # odsunięcie od dolnej krawędzi
        )
