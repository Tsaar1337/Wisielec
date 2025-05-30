from functools import partial

import arcade
from arcade.gui import UILabel, UIInputText


# Funkcje odpowiadające za pokazywanie błedy w GUI(Walidacja)
def clear_error_label(delta_time: float, text_label: UILabel):
    text_label.text = ""


def schedule_clear_error_label(text_label: UILabel, delay: float = 2.0):
    arcade.schedule(partial(clear_error_label, text_label=text_label), delay)


# Podstawowy widok zeby nie pisac ciagle funkcji
class BaseView(arcade.View):
    def __init__(self, back_view=None):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.back_view = back_view

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.manager.enable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE and self.back_view:
            self.window.show_view(self.back_view)


# Gwiazdkowanie hasła
class PasswordInput(UIInputText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.real_text = ""

    def on_event(self, event):
        handled = super().on_event(event)

        if len(self.text) > len(self.real_text):
            add_char = self.text[len(self.real_text)]
            self.real_text += add_char
        elif len(self.text) < len(self.real_text):
            self.real_text = self.real_text[:len(self.text)]

        self.text = "*" * len(self.real_text)

        return handled

    def get_real_text(self):
        return self.real_text
