

import arcade
from arcade.gui import UIAnchorLayout, UIBoxLayout, UILabel, UIGridLayout

from Logic.database_logic import get_all_users_order_by_wins
from UserInterface.view_utils import BaseView


class ScoreboardView(BaseView):
    def __init__(self, back_view):
        super().__init__(back_view)

        main_label = UILabel(text="Wyniki", width=1000, text_color=arcade.color.BLACK, font_size=100, font_name=self.font)

        title_box = UIBoxLayout(vertical=True, space_between=20)

        users = get_all_users_order_by_wins()
        row_count = len(users) + 1  # 1 for headers

        # Jeden wspólny grid z 3 kolumnami (nazwa, wygrane, przegrane)
        scoreboard_grid_layout = UIGridLayout(
            column_count=3,
            row_count=row_count,
            horizontal_spacing=50,
            vertical_spacing=10
        )

        # Nagłówki kolumn
        name_label = UILabel(text="Nazwa", width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)
        wins_label = UILabel(text="Wygrane", width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)
        losses_label = UILabel(text="Przegrane", width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)

        scoreboard_grid_layout.add(column=0, row=0, child=name_label)
        scoreboard_grid_layout.add(column=1, row=0, child=wins_label)
        scoreboard_grid_layout.add(column=2, row=0, child=losses_label)

        # Dane użytkowników
        for i, user in enumerate(users[:6], start=1):
            username_label = UILabel(text=user.name, width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)
            user_wins_label = UILabel(text=str(user.wins), width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)
            user_losses_label = UILabel(text=str(user.losses), width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)

            scoreboard_grid_layout.add(column=0, row=i, child=username_label)
            scoreboard_grid_layout.add(column=1, row=i, child=user_wins_label)
            scoreboard_grid_layout.add(column=2, row=i, child=user_losses_label)

        # Dodanie etykiety tytułu i siatki do UI
        title_box.add(main_label)

        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )
        self.anchor.add(
            child=scoreboard_grid_layout,
            anchor_x="center",
            anchor_y="center",
            align_y=-100
        )
