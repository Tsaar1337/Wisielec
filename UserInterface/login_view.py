import hashlib

import arcade
from arcade.gui import UIFlatButton, UILabel, UIBoxLayout, UIInputText, UIGridLayout

from Database.database_logic import login
from UserInterface.view_utils import schedule_clear_error_label, BaseView, PasswordInput


class LoginView(BaseView):

    def __init__(self):
        super().__init__()


        # Tekst
        main_label = UILabel(text="Logowanie do systemu", width=300, text_color=arcade.color.BLACK, font_size=20,
                             font_name=self.font)
        login_label = UILabel(text="Login", width=50, text_color=arcade.color.BLACK, font_size=10, font_name=self.font)
        password_label = UILabel(text="Hasło", width=50, text_color=arcade.color.BLACK, font_size=10, font_name=self.font)
        error_label = UILabel(text=" ", text_color=arcade.color.RED, font_size=12)

        # Pola wpisywane przez uzytkownika
        input_username_text = UIInputText(text="", width=200, border_color=arcade.color.BLACK,
                                          text_color=arcade.color.BLACK)
        input_password_text = PasswordInput(text="", width=200, border_color=arcade.color.BLACK,
                                            text_color=arcade.color.BLACK)

        # Przyciski
        login_button = UIFlatButton(text="Zaloguj", width=120, font_name=self.font)
        register_button = UIFlatButton(text="Zarejestruj", width=120, font_name=self.font)
        quit_button = UIFlatButton(text="Wyjdź", width=120, font_name=self.font)

        # Oblsluga przycisku login
        @login_button.event("on_click")
        def on_click_login_button(event):
            username = input_username_text.text
            password = input_password_text.get_real_text()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            user = login(username, hashed_password)

            if user:
                print("Zalogowano")
                self.window.user_one = user
                self.window.main_view.user_label.text = username
                self.window.show_view(self.window.main_view)
            else:
                print("Nie zalogowano")
                error_label.text = "Nieprawidłowa nazwa użytkownika lub hasło"
                schedule_clear_error_label(error_label, 2)

        # Oblsluga przycisku register
        @register_button.event("on_click")
        def on_click_register_button(event):
            self.window.show_view(self.window.register_view)
            pass

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            arcade.exit()

        # Inicjalizacja layoutow
        main_box = UIBoxLayout(vertical=True, space_between=20)
        grid_layout = UIGridLayout(column_count=2, row_count=2, horizontal_spacing=20, vertical_spacing=10)
        button_box = UIBoxLayout(vertical=False, space_between=20)

        # Dodanie elemntow do grid layoutu
        grid_layout.add(column=0, row=0, child=login_label)
        grid_layout.add(column=1, row=0, child=input_username_text)
        grid_layout.add(column=0, row=1, child=password_label)
        grid_layout.add(column=1, row=1, child=input_password_text)

        # Dodanie elemntow do boxa z przyciskami
        button_box.add(login_button)
        button_box.add(register_button)

        # Dodanie elemntow do boxa glownego i layoutu
        main_box.add(main_label)
        main_box.add(grid_layout)
        main_box.add(button_box)
        main_box.add(error_label)
        self.anchor.add(child=main_box)
        self.anchor.add(child=quit_button, anchor_x="left", anchor_y="bottom", align_x=35, align_y=35)
