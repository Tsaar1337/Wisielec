import arcade
from arcade.gui import UIFlatButton, UIManager, UIAnchorLayout, UILabel, UIBoxLayout, UIInputText, UIGridLayout, \
    UIMouseFilterMixin, NinePatchTexture
from arcade.gui.experimental import UIScrollArea

from Database import Session, Category
from Logic.database_logic import get_random_word_from_category
from UserInterface.view_utils import BaseView



class SubMenu(UIMouseFilterMixin, UIAnchorLayout):
    def __init__(self,game_view):
        super().__init__(size_hint=(1,1))
        self.game_view = game_view
        font = "Comic Sans MS"

        frame = self.add(UIAnchorLayout(width=400, height=650, size_hint=None))
        frame.with_padding(all=20)

        frame.with_background(
            texture=arcade.gui.NinePatchTexture(
                left=7,
                right=7,
                bottom=7,
                top=7,
                texture=arcade.load_texture(
                    ":resources:gui_basic_assets/window/grey_panel.png"
                ),
            )
        )

        # Nagłówek
        category_label = UILabel(
            text="Wybierz kategorię",
            font_size=20,
            text_color=arcade.color.BLACK,
            width=280,
            font_name=font
        )
        anchor_label = UIAnchorLayout()
        anchor_label.add(category_label, anchor_x="center", anchor_y="top", align_y=0,)
        frame.add(anchor_label)

        # Layout pionowy na przyciski
        button_box = UIBoxLayout(vertical=True, align="center", space_between=10)

        # Pobierz kategorie z bazy danych
        session = Session()
        categories = session.query(Category).all()
        session.close()

        # Dla każdej kategorii twórz przycisk
        for category in categories:
            button = UIFlatButton(text=category.name, width=170)


            @button.event("on_click")
            def on_click_button(event, name=category.name):
                word= get_random_word_from_category(name)
                print(f"Kliknięto kategorię: {name}")
                self.game_view.start_game_with_word(word)

            button_box.add(button)

        frame.add(button_box, anchor_x="center", anchor_y="center",align_y=-25)

    def __del__(self):
        print("Submenu destructor")


class GameView(BaseView):
    MAX_ERRORS = 6
    def __init__(self, back_view):
        super().__init__(back_view)
        self.back_view = self.window.menu_game_view
        self.sub_menu = SubMenu(self)
        self.sub_menu.visible = True

        self.anchor.add(child=self.sub_menu, anchor_x="center", anchor_y="center")

        # Label do wyświetlania słowa wisielca
        self.word_label = UILabel(text="", font_size=36, text_color=arcade.color.BLACK, width=600, multiline=False)
        self.anchor.add(child=self.word_label, anchor_x="center", anchor_y="center", align_y=-150)

        # Inicjuj zmienne na później
        self.letters_layout = None
        self.letter_buttons = []
        self.guessed_letters = set()
        self.errors = 0
        #Informacja o Wygrana/Przegrana
        self.message_label = UILabel(text="", font_size=24, text_color=arcade.color.RED, width=600, multiline=False)
        self.anchor.add(child=self.message_label, anchor_x="center", anchor_y="center", align_y=-100)

    def start_game_with_word(self, word):
        print(f"Start gry ze słowem: {word.word}")
        self.current_word = word.word.lower()
        self.sub_menu.visible = False
        self.visible = True

        # Utwórz maskę - same podkreślenia na początek
        self.masked_word = "_" * len(self.current_word)

        # Wyświetl maskę w labelu
        self.word_label.text = " ".join(self.masked_word)

        # Jeśli był wcześniej layout z literami, usuń go
        if self.letters_layout:
            self.anchor.remove(self.letters_layout)
            self.letters_layout = None

        # Litery A-Z plus polskie znaki
        letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        polish_letters = ['Ą', 'Ć', 'Ę', 'Ł', 'Ń', 'Ó', 'Ś', 'Ź', 'Ż']
        all_letters = letters + polish_letters

        # Dzielimy listę na 2 części
        first_row_letters = all_letters[:17]
        second_row_letters = all_letters[17:]

        # Tworzymy dwa poziome layouty
        first_row_layout = UIBoxLayout(vertical=False, space_between=5)
        second_row_layout = UIBoxLayout(vertical=False, space_between=5)

        self.letter_buttons = []
        self.guessed_letters = set()
        self.errors = 0

        # Dodajemy przyciski do pierwszego wiersza
        for letter in first_row_letters:
            button = UIFlatButton(text=letter, width=50, height=50)
            button.on_click = lambda event, l=letter: self.on_letter_click(l)
            self.letter_buttons.append(button)
            first_row_layout.add(button)

        # Dodajemy przyciski do drugiego wiersza
        for letter in second_row_letters:
            button = UIFlatButton(text=letter, width=50, height=50)
            button.on_click = lambda event, l=letter: self.on_letter_click(l)
            self.letter_buttons.append(button)
            second_row_layout.add(button)

        # Tworzymy pionowy layout, który będzie zawierał oba wiersze
        self.letters_layout = UIBoxLayout(vertical=True, space_between=5)
        self.letters_layout.add(first_row_layout)
        self.letters_layout.add(second_row_layout)

        # Dodajemy całość do anchor
        self.anchor.add(child=self.letters_layout, anchor_x="center", anchor_y="bottom", align_y=40)

        # Włącz wszystkie przyciski na nową grę
        for button in self.letter_buttons:
            button.disabled = False

    def on_letter_click(self, letter):
        letter_lower = letter.lower()
        if letter_lower in self.guessed_letters:
            return  # już sprawdzaliśmy tę literę, ignoruj

        self.guessed_letters.add(letter_lower)

        # Wyłącz przycisk, żeby nie dało się klikać ponownie
        for button in self.letter_buttons:
            if button.text == letter:
                button.disabled = True
                break

        if letter_lower in self.current_word:
            print(f"Litera '{letter}' jest w słowie!")
            self.update_display()
            # Sprawdź, czy wygrałeś
            if "_" not in self.masked_word:
                self.message_label.text = "Wygrałeś!!!"
                for button in self.letter_buttons:
                    button.disabled = True

        else:
            self.errors += 1
            print(f"Litera '{letter}' nie ma w słowie! Błędów: {self.errors}/{self.MAX_ERRORS}")

            if self.errors >= self.MAX_ERRORS:
                self.message_label.text = "Przegrałeś! Przekroczono maksymalną liczbę błędów."
                for button in self.letter_buttons:
                    button.disabled = True

    def update_display(self):
        display_word = [letter if letter in self.guessed_letters else "_" for letter in self.current_word]
        self.masked_word = "".join(display_word)
        self.word_label.text = " ".join(display_word)

    def __del__(self):
        print("GameView został usunięty z pamięci.")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE and self.back_view:
            self.window.show_view(self.back_view)

            self.manager.clear()
            self.manager.disable()

            # Zerujemy referencję do GameView w SubMenu
            if self.sub_menu:
                self.sub_menu.game_view = None
            self.sub_menu = None

            # Zerujemy inne referencje
            self.back_view = None
            self.word_label = None
            self.current_word = None
            self.masked_word = None

            # Usuwamy z menu_game_view.game_view
            if hasattr(self.window.menu_game_view, "game_view"):
                self.window.menu_game_view.game_view = None

            # Wymuszenie garbage collection
            import gc
            gc.collect()

    def draw_hangman(self):
        base_x = 1000
        base_y = 1500
        print("[DEBUG] Rysuję wisielca")

        # Szubienica
        arcade.draw_line(base_x, base_y, base_x + 100, base_y, arcade.color.BLACK, 4)  # podstawa
        arcade.draw_line(base_x + 50, base_y, base_x + 50, base_y + 200, arcade.color.BLACK, 4)  # słup
        arcade.draw_line(base_x + 50, base_y + 200, base_x + 120, base_y + 200, arcade.color.BLACK, 4)  # belka
        arcade.draw_line(base_x + 120, base_y + 200, base_x + 120, base_y + 170, arcade.color.BLACK, 4)
        print("[DEBUG] Narysowalem szubienice")

        # Głowa
        if self.errors >= 1:
            arcade.draw_circle_outline(base_x + 120, base_y + 150, 20, arcade.color.BLACK, 4)

        # Tułów
        if self.errors >= 2:
            arcade.draw_line(base_x + 120, base_y + 130, base_x + 120, base_y + 90, arcade.color.BLACK, 4)

        # Ręce
        if self.errors >= 3:
            arcade.draw_line(base_x + 120, base_y + 120, base_x + 100, base_y + 110, arcade.color.BLACK, 4)
        if self.errors >= 4:
            arcade.draw_line(base_x + 120, base_y + 120, base_x + 140, base_y + 110, arcade.color.BLACK, 4)

        # Nogi
        if self.errors >= 5:
            arcade.draw_line(base_x + 120, base_y + 90, base_x + 100, base_y + 70, arcade.color.BLACK, 4)
        if self.errors >= 6:
            arcade.draw_line(base_x + 120, base_y + 90, base_x + 140, base_y + 70, arcade.color.BLACK, 4)

    def on_draw(self):
        print("[DEBUG] on_draw działa")
        self.draw_hangman()
        super().on_draw()