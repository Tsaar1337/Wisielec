import arcade
from arcade.gui import UIFlatButton, UIManager, UIAnchorLayout, UILabel, UIBoxLayout, UIInputText, UIGridLayout
from docutils.nodes import title

from .game_view import GameView
from UserInterface.view_utils import schedule_clear_error_label, BaseView


class MenuGameView(BaseView):

    def __init__(self, back_view):
        super().__init__(back_view)

        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(text="Wybierz tryb gry", width=1000, text_color=arcade.color.BLACK, font_size=100,
                             font_name=self.font)
        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )
        error_label = UILabel(text=" ", text_color=arcade.color.RED, font_size=12)


        play_time_button = UIFlatButton(text="Na Czas", width=200)
        play_oponent_button = UIFlatButton(text="Przeciwko sobie", width=200)
        play_health_button = UIFlatButton(text="Na życia", width=200)
        info_button = UIFlatButton(text="Informacje", width=200)

        @play_time_button.event("on_click")
        def on_click_play_time(event):
            self.window.game_view.time_mode = True
            self.window.show_view(self.window.game_view_on_time)

        @play_health_button.event("on_click")
        def on_click_play_health(event):
            self.window.game_view.time_mode = False
            self.window.show_view(self.window.game_view)

        @play_oponent_button.event("on_click")
        def on_click_play_opponent(event):
            # error_label.text = "Gra wymaga zalogowania druiego użytkownika"
            # schedule_clear_error_label(error_label, 2)
            self.window.show_view(self.window.two_player_game_view)
        @info_button.event("on_click")
        def on_click_info(event):
            self.window.show_view(self.window.info_view)





        main_box = UIBoxLayout(vertical=True, space_between=20)
        grid_layout = UIGridLayout(column_count=2, row_count=3, horizontal_spacing=20, vertical_spacing=10)

        grid_layout.add(column=0, row=0, child=play_time_button)
        grid_layout.add(column=1, row=0, child=play_health_button)
        grid_layout.add(column=0, row=1, child=play_oponent_button)
        grid_layout.add(column=1, row=1, child=info_button)

        main_box.add(grid_layout)
        main_box.add(error_label)
        self.anchor.add(child=main_box)



