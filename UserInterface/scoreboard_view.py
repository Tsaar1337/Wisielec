import arcade
from arcade.gui import UIAnchorLayout, UIBoxLayout, UILabel, UIGridLayout

from Logic.database_logic import get_all_users_order_by_wins
from UserInterface.view_utils import BaseView


class ScoreboardView(BaseView):
    def __init__(self, back_view):
        super().__init__(back_view)

        self.username_labels = []
        self.wins_labels = []
        self.losses_labels = []

        main_label = UILabel(text="Wyniki", width=1000, text_color=arcade.color.BLACK, font_size=100, font_name=self.font)

        title_box = UIBoxLayout(vertical=True, space_between=20)

        row_count = 7  # 1 nagłówek + max 6 graczy

        self.scoreboard_grid_layout = UIGridLayout(
            column_count=3,
            row_count=row_count,
            horizontal_spacing=50,
            vertical_spacing=10
        )

        # Nagłówki
        name_label = UILabel(text="Nazwa", width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)
        wins_label = UILabel(text="Wygrane", width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)
        losses_label = UILabel(text="Przegrane", width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)

        self.scoreboard_grid_layout.add(column=0, row=0, child=name_label)
        self.scoreboard_grid_layout.add(column=1, row=0, child=wins_label)
        self.scoreboard_grid_layout.add(column=2, row=0, child=losses_label)

        # Predefiniowane puste etykiety na dane użytkowników
        for i in range(1, 7):
            username_label = UILabel(text="", width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)
            user_wins_label = UILabel(text="", width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)
            user_losses_label = UILabel(text="", width=200, text_color=arcade.color.BLACK, font_size=30, font_name=self.font)

            self.username_labels.append(username_label)
            self.wins_labels.append(user_wins_label)
            self.losses_labels.append(user_losses_label)

            self.scoreboard_grid_layout.add(column=0, row=i, child=username_label)
            self.scoreboard_grid_layout.add(column=1, row=i, child=user_wins_label)
            self.scoreboard_grid_layout.add(column=2, row=i, child=user_losses_label)

        # UI dodanie
        title_box.add(main_label)

        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )
        self.anchor.add(
            child=self.scoreboard_grid_layout,
            anchor_x="center",
            anchor_y="center",
            align_y=-100
        )


    def update_scoreboard(self):
        users = get_all_users_order_by_wins()

        for i in range(6):
            if i < len(users):
                user = users[i]
                self.username_labels[i].text = user.name
                self.wins_labels[i].text = str(user.wins)
                self.losses_labels[i].text = str(user.losses)
            else:
                # Wyczyść puste wiersze
                self.username_labels[i].text = ""
                self.wins_labels[i].text = ""
                self.losses_labels[i].text = ""

    def on_show_view(self):
        super().on_show_view()
        self.update_scoreboard()
