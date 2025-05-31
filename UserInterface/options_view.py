import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UISlider
from UserInterface.view_utils import BaseView


class Options(BaseView):
    def __init__(self, back_view):
        super().__init__(back_view)


        # Tytuł
        title_box = UIBoxLayout(vertical=True, space_between=20)
        main_label = UILabel(
            text="Ustawienia",
            font_size=60,
            text_color=arcade.color.BLACK,
            width=600,
            font_name=self.font
        )

        title_box.add(main_label)
        self.anchor.add(
            child=title_box,
            anchor_x="center",
            anchor_y="top",
            align_y=-30
        )

        # Kontener na głośność
        volume_box = UIBoxLayout(vertical=True, space_between=20)

        # Label pokazujący głośność
        self.volume_label = UILabel(
            text=f"Głośność: {int(self.window.volume * 100)}%",
            font_size=30,
            text_color=arcade.color.BLACK
        )
        volume_box.add(self.volume_label)

        # Suwak do regulacji głośności
        self.volume_slider = UISlider(
            value=self.window.volume,
            min_value=0.0,
            max_value=1.0,
            width=300,
            step=0.01
        )
        self.volume_slider.on_change = self.on_volume_change
        volume_box.add(self.volume_slider)

        self.anchor.add(
            child=volume_box,
            anchor_x="center",
            anchor_y="center",
            align_y=-50
        )

    def on_volume_change(self, event):
        new_volume = self.volume_slider.value
        self.window.volume = new_volume
        self.update_volume_label()
        self.set_music_volume(new_volume)

    def update_volume_label(self):
        self.volume_label.text = f"Głośność: {int(self.window.volume * 100)}%"

    def set_music_volume(self, volume):
        if self.window.music_player:
            try:
                # Zmiana głośnośći "na żwo"
                self.window.music_player.volume = volume
            except AttributeError:
                # Jak nie pójdzie, to restartujemy muzykę z nową głośnością
                self.window.music_player.pause()
                self.window.music_player = self.window.background_music.play(volume=volume, loop=True)
