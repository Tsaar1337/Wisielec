import arcade
from arcade.gui import UIFlatButton, UIManager, UIAnchorLayout, UILabel, UIBoxLayout, UIInputText, UIGridLayout
from docutils.nodes import title

from UserInterface.view_utils import schedule_clear_error_label, BaseView


class MenuGameView(BaseView):

    def __init__(self):
        super().__init__()
        font = "Comic sans MS"
        self.back_view=self.window.main_view
        self.anchor = self.manager.add(UIAnchorLayout())
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(text="Wybierz tryb gry", width=1000, text_color=arcade.color.BLACK, font_size=100,
                             font_name=font)
        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )
        error_label = UILabel(text=" ", text_color=arcade.color.RED, font_size=12)

        PlayTime_button = UIFlatButton(text="Na Czas", width=200)
        PlayOponent_button = UIFlatButton(text="Przeciwko sobie", width=200)
        PlayHealth_button = UIFlatButton(text="Na życia", width=200)
        Info_button = UIFlatButton(text="Informacje", width=200)

        @PlayTime_button.event("on_click")
        def on_click_back(event):
            self.window.show_view(self.window.game_view)

        @PlayHealth_button.event("on_click")
        def on_click_back(event):
            self.window.show_view(self.window.game_view)

        @PlayOponent_button.event("on_click")
        def on_click_back(event):
            error_label.text = "Gra wymaga zalogowania druiego użytkownika"
            schedule_clear_error_label(error_label, 2)

        @Info_button.event("on_click")
        def on_click_back(event):
            self.window.show_view(self.window.info_view)





        main_box = UIBoxLayout(vertical=True, space_between=20)
        grid_layout = UIGridLayout(column_count=2, row_count=3, horizontal_spacing=20, vertical_spacing=10)

        grid_layout.add(column=0, row=0, child=PlayTime_button)
        grid_layout.add(column=1, row=0, child=PlayHealth_button)
        grid_layout.add(column=0, row=1, child=PlayOponent_button)
        grid_layout.add(column=1, row=1, child=Info_button)

        main_box.add(grid_layout)
        main_box.add(error_label)
        self.anchor.add(child=main_box)

