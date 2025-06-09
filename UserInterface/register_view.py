import hashlib
import re
import arcade
from arcade.gui import UIFlatButton, UILabel, UIBoxLayout, UIInputText, UIGridLayout
from Database.database_logic import register
from UserInterface.view_utils import schedule_clear_error_label, BaseView, PasswordInput


class RegisterView(BaseView):
    """Widok formularza rejestracji użytkownika.

    Klasa odpowiedzialna za obsługę procesu rejestracji nowego użytkownika w systemie.
    Zapewnia interfejs użytkownika z polami do wprowadzenia loginu i hasła oraz
    mechanizmy walidacji wprowadzonych danych.

    Args:
        back_view: Widok, do którego nastąpi powrót po anulowaniu rejestracji.

    Attributes:
        anchor: Główny kontener dla elementów UI.
    """

    def __init__(self, back_view):
        """Inicjalizuje widok rejestracji.

        Tworzy kompletny interfejs użytkownika zawierający:
        - Tytuł formularza
        - Pola wprowadzania loginu i hasła
        - Przycisk rejestracji
        - Etykietę błędów
        
        Implementuje również logikę walidacji i przetwarzania formularza rejestracji.

        Args:
            back_view: Referencja do poprzedniego widoku.
        """
        super().__init__(back_view)

        # Tworzenie etykiet
        main_label = UILabel(
            text="Rejestracja do systemu",
            width=300,
            text_color=arcade.color.BLACK,
            font_size=20,
            font_name=self.font
        )
        login_label = UILabel(
            text="Login",
            width=50,
            text_color=arcade.color.BLACK,
            font_size=10,
            font_name=self.font
        )
        password_label = UILabel(
            text="Hasło",
            width=50,
            text_color=arcade.color.BLACK,
            font_size=10,
            font_name=self.font
        )
        password_label2 = UILabel(
            text="Hasło",
            width=50,
            text_color=arcade.color.BLACK,
            font_size=10,
            font_name=self.font
        )

        # Tworzenie pól wprowadzania danych
        input_username_text = UIInputText(
            text="",
            width=200,
            border_color=arcade.color.BLACK,
            text_color=arcade.color.BLACK
        )
        input_password_text = PasswordInput(
            text="",
            width=200,
            border_color=arcade.color.BLACK,
            text_color=arcade.color.BLACK
        )
        input_password2_text = PasswordInput(
            text="",
            width=200,
            border_color=arcade.color.BLACK,
            text_color=arcade.color.BLACK
        )

        # Tworzenie przycisku rejestracji i etykiety błędów
        register_button = UIFlatButton(text="Zarejestruj", width=200, font_name=self.font)
        error_label = UILabel(text=" ", text_color=arcade.color.RED, font_size=12)

        @register_button.event("on_click")
        def on_click_register_button(event):
            """Obsługuje zdarzenie kliknięcia przycisku rejestracji.

            Waliduje wprowadzone dane i przeprowadza proces rejestracji użytkownika.
            W przypadku błędów wyświetla odpowiednie komunikaty.

            Przeprowadzane walidacje:
            - Sprawdzenie czy pola nie są puste
            - Sprawdzenie czy nie zawierają białych znaków
            - Sprawdzenie czy hasła są identyczne
            - Sprawdzenie czy użytkownik o danym loginie nie istnieje

            Args:
                event: Obiekt zdarzenia kliknięcia (niewykorzystywany).
            """
            username = input_username_text.text
            password = input_password_text.get_real_text()
            password2 = input_password2_text.get_real_text()
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Walidacja danych
            if not self._validate_registration_data(username, password, password2, error_label):
                return

            # Próba rejestracji użytkownika
            if not register(username, hashed_password):
                error_label.text = "Użytkownik o danym loginie już istnieje"
                schedule_clear_error_label(error_label, 2)
                return

            print("Zerejestrowano")
            self.window.show_view(self.window.login_view)

        # Konfiguracja układu UI
        self._setup_ui_layout(
            main_label, login_label, password_label, password_label2,
            input_username_text, input_password_text, input_password2_text,
            register_button, error_label
        )

    def _validate_registration_data(self, username, password, password2, error_label):
        """Waliduje dane wprowadzone w formularzu rejestracji.

        Args:
            username (str): Wprowadzona nazwa użytkownika.
            password (str): Wprowadzone hasło.
            password2 (str): Powtórzone hasło.
            error_label (UILabel): Etykieta do wyświetlania błędów.

        Returns:
            bool: True jeśli dane są poprawne, False w przeciwnym razie.
        """
        if not username:
            error_label.text = "Login nie może byś pusty"
            schedule_clear_error_label(error_label, 2)
            return False
        
        if re.search(r"\s", username):
            error_label.text = "Login nie może zawierać białych znaków"
            schedule_clear_error_label(error_label, 2)
            return False
            
        if not password or not password2:
            error_label.text = "Hasła nie mogą być puste"
            schedule_clear_error_label(error_label, 2)
            return False
            
        if re.search(r"\s", password) or re.search(r"\s", password2):
            error_label.text = "Hasła nie mogą zawierać białych znaków"
            schedule_clear_error_label(error_label, 2)
            return False
            
        if password != password2:
            error_label.text = "Hasła sie nie zgadzaja"
            schedule_clear_error_label(error_label, 2)
            return False
            
        return True

    def _setup_ui_layout(self, main_label, login_label, password_label, password_label2,
                        input_username_text, input_password_text, input_password2_text,
                        register_button, error_label):
        """Konfiguruje układ elementów interfejsu użytkownika.

        Args:
            main_label (UILabel): Główna etykieta formularza.
            login_label (UILabel): Etykieta pola loginu.
            password_label (UILabel): Etykieta pierwszego pola hasła.
            password_label2 (UILabel): Etykieta drugiego pola hasła.
            input_username_text (UIInputText): Pole wprowadzania loginu.
            input_password_text (PasswordInput): Pierwsze pole wprowadzania hasła.
            input_password2_text (PasswordInput): Drugie pole wprowadzania hasła.
            register_button (UIFlatButton): Przycisk rejestracji.
            error_label (UILabel): Etykieta błędów.
        """
        main_box = UIBoxLayout(vertical=True, space_between=20)
        grid_layout = UIGridLayout(
            column_count=2,
            row_count=3,
            horizontal_spacing=20,
            vertical_spacing=10
        )

        # Dodawanie elementów do układu siatki
        grid_layout.add(column=0, row=0, child=login_label)
        grid_layout.add(column=1, row=0, child=input_username_text)
        grid_layout.add(column=0, row=1, child=password_label)
        grid_layout.add(column=1, row=1, child=input_password_text)
        grid_layout.add(column=0, row=2, child=password_label2)
        grid_layout.add(column=1, row=2, child=input_password2_text)

        # Składanie głównego układu
        main_box.add(main_label)
        main_box.add(grid_layout)
        main_box.add(register_button)
        main_box.add(error_label)
        self.anchor.add(child=main_box)