import hashlib
import re

import arcade
from arcade.gui import UIFlatButton, UIManager, UIAnchorLayout, UILabel, UIBoxLayout, UIInputText, UIGridLayout

from Database.models import User
from Database.session import Session
from Logic.database_logic import register
from UserInterface.login_view import LoginView
from UserInterface.main_menu import MainMenu
from UserInterface.view_utils import schedule_clear_error_label, BaseView, PasswordInput


class RegisterView(BaseView):

    def __init__(self, back_view):
        super().__init__(back_view)

        main_label = UILabel(text="Rejestracja do systemu", width=300, text_color=arcade.color.BLACK,
                              font_size=20, font_name=self.font)
        login_label = UILabel(text="Login", width=50, text_color=arcade.color.BLACK, font_size=10, font_name=self.font)
        password_label = UILabel(text="Hasło", width=50, text_color=arcade.color.BLACK, font_size=10, font_name=self.font)
        password_label2 = UILabel(text="Hasło", width=50, text_color=arcade.color.BLACK, font_size=10, font_name=self.font)

        input_username_text = UIInputText(text="", width=200, border_color=arcade.color.BLACK, text_color=arcade.color.BLACK)
        input_password_text = PasswordInput(text="", width=200, border_color=arcade.color.BLACK, text_color=arcade.color.BLACK)
        input_password2_text = PasswordInput(text="", width=200, border_color=arcade.color.BLACK, text_color=arcade.color.BLACK)

        register_button = UIFlatButton(text="Zarejestruj", width=200, font_name=self.font)
        error_label = UILabel(text=" ", text_color=arcade.color.RED, font_size=12)

        @register_button.event("on_click")
        def on_click_register_button(event):
            username = input_username_text.text
            password = input_password_text.get_real_text()
            password2 = input_password2_text.get_real_text()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if not username:
                error_label.text = "Login nie może byś pusty"
                schedule_clear_error_label(error_label, 2)
                return
            if re.search(r"\s", username):
                error_label.text="Login nie może zawierać białych znaków"
                schedule_clear_error_label(error_label, 2)
                return
            if not password or not password2:
                error_label.text="Hasła nie mogą być puste"
                schedule_clear_error_label(error_label, 2)
                return
            if re.search(r"\s", password) or re.search(r"\s", password2):
                error_label.text="Hasła nie mogą zawierać białych znaków"
                schedule_clear_error_label(error_label, 2)
                return
            if password != password2:
                error_label.text="Hasła sie nie zgadzaja"
                schedule_clear_error_label(error_label, 2)
                return
            if not register(username, hashed_password):
                error_label.text="Użytkownik o danym loginie już istnieje"
                schedule_clear_error_label(error_label, 2)
                return
            print("Zerejestrowano")
            self.window.show_view(self.window.login_view)


        main_box = UIBoxLayout(vertical=True, space_between=20)
        grid_layout = UIGridLayout(column_count=2, row_count=3, horizontal_spacing=20, vertical_spacing=10 )

        grid_layout.add(column=0, row=0, child=login_label)
        grid_layout.add(column=1 ,row=0, child=input_username_text)

        grid_layout.add(column=0, row=1, child=password_label)
        grid_layout.add(column=1, row=1, child=input_password_text)

        grid_layout.add(column=0, row=2, child=password_label2)
        grid_layout.add(column=1, row=2, child=input_password2_text)


        main_box.add(main_label)
        main_box.add(grid_layout)
        main_box.add(register_button)
        main_box.add(error_label)
        self.anchor.add(child=main_box)






