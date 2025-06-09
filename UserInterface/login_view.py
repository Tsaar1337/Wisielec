"""
Moduł implementujący widok logowania do systemu gry Wisielec.
Zapewnia interfejs do uwierzytelniania użytkowników oraz nawigację do rejestracji.
"""

import hashlib
import arcade
from arcade.gui import UIFlatButton, UILabel, UIBoxLayout, UIInputText, UIGridLayout
from Database.database_logic import login
from UserInterface.view_utils import schedule_clear_error_label, BaseView, PasswordInput


class LoginView(BaseView):
    """Widok logowania do systemu gry.

    Implementuje interfejs logowania zawierający:
    - Pola do wprowadzania nazwy użytkownika i hasła
    - Przyciski logowania, rejestracji i wyjścia
    - Obsługę błędów logowania
    """

    def __init__(self):
        """Inicjalizuje widok logowania.

        Tworzy kompletny interfejs użytkownika z polami do wprowadzania danych,
        przyciskami akcji oraz obsługą zdarzeń.
        """
        super().__init__()
        
        self.input_fields = self._create_input_fields()
        self.labels = self._create_labels()
        self.buttons = self._create_buttons()
        
        self._setup_button_handlers()
        self._setup_layout()

    def _create_labels(self):
        """Tworzy etykiety interfejsu.

        Returns:
            dict: Słownik zawierający utworzone etykiety:
                - main_label: Tytuł widoku
                - login_label: Etykieta pola loginu
                - password_label: Etykieta pola hasła
                - error_label: Etykieta błędów
        """
        return {
            'main_label': UILabel(
                text="Logowanie do systemu",
                width=300,
                text_color=arcade.color.BLACK,
                font_size=20,
                font_name=self.font
            ),
            'login_label': UILabel(
                text="Login",
                width=50,
                text_color=arcade.color.BLACK,
                font_size=10,
                font_name=self.font
            ),
            'password_label': UILabel(
                text="Hasło",
                width=50,
                text_color=arcade.color.BLACK,
                font_size=10,
                font_name=self.font
            ),
            'error_label': UILabel(
                text=" ",
                text_color=arcade.color.RED,
                font_size=12
            )
        }

    def _create_input_fields(self):
        """Tworzy pola wprowadzania danych.

        Returns:
            dict: Słownik zawierający utworzone pola:
                - username: Pole nazwy użytkownika
                - password: Pole hasła
        """
        return {
            'username': UIInputText(
                text="",
                width=200,
                border_color=arcade.color.BLACK,
                text_color=arcade.color.BLACK
            ),
            'password': PasswordInput(
                text="",
                width=200,
                border_color=arcade.color.BLACK,
                text_color=arcade.color.BLACK
            )
        }

    def _create_buttons(self):
        """Tworzy przyciski interfejsu.

        Returns:
            dict: Słownik zawierający utworzone przyciski:
                - login: Przycisk logowania
                - register: Przycisk rejestracji
                - quit: Przycisk wyjścia
        """
        return {
            'login': UIFlatButton(
                text="Zaloguj",
                width=120,
                font_name=self.font
            ),
            'register': UIFlatButton(
                text="Zarejestruj",
                width=120,
                font_name=self.font
            ),
            'quit': UIFlatButton(
                text="Wyjdź",
                width=120,
                font_name=self.font
            )
        }

    def _setup_button_handlers(self):
        """Konfiguruje obsługę zdarzeń dla przycisków.

        Definiuje zachowanie systemu po:
        - Próbie logowania
        - Przejściu do rejestracji
        - Wyjściu z aplikacji
        """
        @self.buttons['login'].event("on_click")
        def on_click_login_button(event):
            """Obsługuje próbę logowania.

            Weryfikuje dane logowania i:
            - W przypadku sukcesu: przechodzi do głównego menu
            - W przypadku błędu: wyświetla komunikat o błędzie
            """
            username = self.input_fields['username'].text
            password = self.input_fields['password'].get_real_text()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            user = login(username, hashed_password)

            if user:
                self.window.user_one = user
                self.window.main_view.user_label.text = username
                self.window.show_view(self.window.main_view)
            else:
                self.labels['error_label'].text = "Nieprawidłowa nazwa użytkownika lub hasło"
                schedule_clear_error_label(self.labels['error_label'], 2)

        @self.buttons['register'].event("on_click")
        def on_click_register_button(event):
            """Przechodzi do widoku rejestracji."""
            self.window.show_view(self.window.register_view)

        @self.buttons['quit'].event("on_click")
        def on_click_quit_button(event):
            """Kończy działanie aplikacji."""
            arcade.exit()

    def _setup_layout(self):
        """Konfiguruje układ elementów interfejsu.

        Organizuje elementy interfejsu w odpowiedniej strukturze
        i pozycjonuje je na ekranie.
        """
        # Utworzenie głównych kontenerów
        main_box = UIBoxLayout(vertical=True, space_between=20)
        grid_layout = UIGridLayout(
            column_count=2,
            row_count=2,
            horizontal_spacing=20,
            vertical_spacing=10
        )
        button_box = UIBoxLayout(vertical=False, space_between=20)

        # Konfiguracja siatki pól wprowadzania
        grid_layout.add(column=0, row=0, child=self.labels['login_label'])
        grid_layout.add(column=1, row=0, child=self.input_fields['username'])
        grid_layout.add(column=0, row=1, child=self.labels['password_label'])
        grid_layout.add(column=1, row=1, child=self.input_fields['password'])

        # Konfiguracja przycisków akcji
        button_box.add(self.buttons['login'])
        button_box.add(self.buttons['register'])

        # Złożenie głównego układu
        main_box.add(self.labels['main_label'])
        main_box.add(grid_layout)
        main_box.add(button_box)
        main_box.add(self.labels['error_label'])

        # Pozycjonowanie elementów
        self.anchor.add(child=main_box)
        self.anchor.add(
            child=self.buttons['quit'],
            anchor_x="left",
            anchor_y="bottom",
            align_x=35,
            align_y=35
        )