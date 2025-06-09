import arcade
from arcade.gui import UIBoxLayout, UILabel, UIGridLayout, UIFlatButton
from Database.database_logic import get_all_users_order_by_wins
from UserInterface.view_utils import BaseView


class ScoreboardView(BaseView):
    """Widok tablicy wyników gry.

    Klasa odpowiedzialna za wyświetlanie i zarządzanie tablicą wyników graczy.
    Prezentuje statystyki graczy w formie tabelarycznej, zawierającej nazwy użytkowników,
    liczbę wygranych i przegranych gier.

    Args:
        back_view: Widok, do którego nastąpi powrót po opuszczeniu tablicy wyników.

    Attributes:
        username_labels (list): Lista etykiet zawierających nazwy użytkowników.
        wins_labels (list): Lista etykiet zawierających liczby wygranych.
        losses_labels (list): Lista etykiet zawierających liczby przegranych.
        scoreboard_grid_layout (UIGridLayout): Układ siatki zawierający tabelę wyników.
    """

    def __init__(self, back_view):
        """Inicjalizuje widok tablicy wyników.

        Tworzy interfejs użytkownika zawierający:
        - Tytuł "Wyniki"
        - Tabelę z nagłówkami (Nazwa, Wygrane, Przegrane)
        - Miejsca na dane maksymalnie 6 graczy
        - Przycisk do eksportu wyników

        Args:
            back_view: Referencja do poprzedniego widoku.
        """
        super().__init__(back_view)

        # Inicjalizacja list na etykiety
        self.username_labels = []
        self.wins_labels = []
        self.losses_labels = []

        # Utworzenie głównego tytułu
        main_label = UILabel(text="Wyniki", width=1000, text_color=arcade.color.BLACK, 
                           font_size=100, font_name=self.font)
        title_box = UIBoxLayout(vertical=True, space_between=20)

        # Konfiguracja układu siatki dla tablicy wyników
        row_count = 7  # 1 nagłówek + max 6 graczy
        self.scoreboard_grid_layout = UIGridLayout(
            column_count=3,
            row_count=row_count,
            horizontal_spacing=50,
            vertical_spacing=10
        )

        # Konfiguracja nagłówków tabeli
        self._setup_headers()
        
        # Przygotowanie pustych etykiet na dane użytkowników
        self._setup_empty_labels()

        # Konfiguracja układu UI
        self._setup_ui_layout(title_box, main_label)
        
        # Dodanie przycisku eksportu
        self._setup_export_button()

    def update_scoreboard(self):
        """Aktualizuje zawartość tablicy wyników.

        Pobiera aktualną listę użytkowników posortowaną według liczby wygranych
        i aktualizuje wyświetlane dane. Jeśli jest mniej niż 6 graczy,
        pozostałe wiersze są czyszczone.
        """
        users = get_all_users_order_by_wins()

        for i in range(6):
            if i < len(users):
                user = users[i]
                self.username_labels[i].text = user.name
                self.wins_labels[i].text = str(user.wins)
                self.losses_labels[i].text = str(user.losses)
            else:
                # Czyszczenie pustych wierszy
                self.username_labels[i].text = ""
                self.wins_labels[i].text = ""
                self.losses_labels[i].text = ""

    def on_show_view(self):
        """Metoda wywoływana przy wyświetleniu widoku.

        Aktualizuje tablicę wyników przy każdym wyświetleniu widoku.
        """
        super().on_show_view()
        self.update_scoreboard()

    def _setup_headers(self):
        """Konfiguruje nagłówki tabeli wyników.

        Metoda pomocnicza tworząca i dodająca etykiety nagłówków do układu siatki.
        """
        headers = [
            ("Nazwa", 0), ("Wygrane", 1), ("Przegrane", 2)
        ]
        for text, column in headers:
            label = UILabel(text=text, width=200, text_color=arcade.color.BLACK, 
                          font_size=30, font_name=self.font)
            self.scoreboard_grid_layout.add(column=column, row=0, child=label)

    def _setup_empty_labels(self):
        """Tworzy puste etykiety dla danych użytkowników.

        Metoda pomocnicza inicjalizująca miejsca na dane maksymalnie 6 graczy.
        """
        for i in range(1, 7):
            username_label = UILabel(text="", width=200, text_color=arcade.color.BLACK, 
                                  font_size=30, font_name=self.font)
            user_wins_label = UILabel(text="", width=200, text_color=arcade.color.BLACK, 
                                    font_size=30, font_name=self.font)
            user_losses_label = UILabel(text="", width=200, text_color=arcade.color.BLACK, 
                                      font_size=30, font_name=self.font)

            self.username_labels.append(username_label)
            self.wins_labels.append(user_wins_label)
            self.losses_labels.append(user_losses_label)

            self.scoreboard_grid_layout.add(column=0, row=i, child=username_label)
            self.scoreboard_grid_layout.add(column=1, row=i, child=user_wins_label)
            self.scoreboard_grid_layout.add(column=2, row=i, child=user_losses_label)

    def _setup_export_button(self):
        """Konfiguruje przycisk eksportu wyników.

        Tworzy i konfiguruje przycisk umożliwiający eksport wyników do pliku tekstowego.
        """
        export_button = UIFlatButton(text="Exportuj wyniki", width=200)
        
        @export_button.event("on_click")
        def on_click_export(event):
            """Obsługa zdarzenia kliknięcia przycisku eksportu.

            Zapisuje aktualny stan tablicy wyników do pliku 'scoreboard.txt'.
            """
            with open("scoreboard.txt", "w") as file:
                for i in range(6):
                    user = get_all_users_order_by_wins()[i]
                    file.write(f"{user.name} {user.wins} {user.losses}\n")

        self.anchor.add(
            child=export_button,
            anchor_x="left",
            anchor_y="top",
            align_x=35,
            align_y=-35
        )

    def _setup_ui_layout(self, title_box, main_label):
        """Konfiguruje główny układ interfejsu użytkownika.

        Ustawia tytuł i tablicę wyników w głównym oknie widoku.
        """
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