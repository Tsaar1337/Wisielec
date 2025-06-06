import time

import arcade
from arcade.gui import UIFlatButton, UIAnchorLayout, UILabel, UIBoxLayout, UIMouseFilterMixin
from pygments.lexers import q

from Database import Session, Category
from Database.database_logic import get_random_word_from_category, add_win_to_user, add_lose_to_user
from UserInterface.view_utils import BaseView



class SubMenu(UIMouseFilterMixin, UIAnchorLayout):
    def __init__(self, game_view):
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
        def create_button(name):
            button = UIFlatButton(text=name, width=170)

            @button.event("on_click")
            def on_click_button(event):
                word = get_random_word_from_category(name)
                print(f"Kliknięto kategorię: {name}")
                self.game_view.start_game_with_word(word)
                self.game_view.is_running = True
                self.game_view.start_time = time.time()

            return button

        for category in categories:
            button = create_button(category.name)
            button_box.add(button)

        frame.add(button_box, anchor_x="center", anchor_y="center",align_y=-25)


    def __del__(self):
        print("Submenu destructor")


class GameView(BaseView):
    MAX_ERRORS = 6

    def __init__(self, back_view, on_time: bool):
        super().__init__(back_view)
        self.back_view = self.window.menu_game_view
        self.sub_menu = SubMenu(self)
        self.sub_menu.visible = True
        self.on_time = on_time
        self.is_running = False


        self.anchor.add(child=self.sub_menu, anchor_x="center", anchor_y="center")

        self.word_label = UILabel(text="", font_size=36, text_color=arcade.color.BLACK, width=600, multiline=False)
        self.anchor.add(child=self.word_label, anchor_x="center", anchor_y="center", align_y=-150)

        self.message_label = UILabel(text="", font_size=24, text_color=arcade.color.RED, width=600, multiline=False)
        self.anchor.add(child=self.message_label, anchor_x="center", anchor_y="center", align_y=-100)

        # Litery
        self.letter_buttons = []
        self.letters_layout = UIBoxLayout(vertical=True, space_between=5)
        self.first_row_layout = UIBoxLayout(vertical=False, space_between=5)
        self.second_row_layout = UIBoxLayout(vertical=False, space_between=5)

        letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        polish_letters = ['Ą', 'Ć', 'Ę', 'Ł', 'Ń', 'Ó', 'Ś', 'Ź', 'Ż']
        all_letters = letters + polish_letters

        for i, letter in enumerate(all_letters):
            button = UIFlatButton(text=letter, width=50, height=50)
            button.on_click = lambda event, l=letter: self.on_letter_click(l)
            self.letter_buttons.append(button)
            if i < 17:
                self.first_row_layout.add(button)
            else:
                self.second_row_layout.add(button)

        self.letters_layout.add(self.first_row_layout)
        self.letters_layout.add(self.second_row_layout)
        self.anchor.add(child=self.letters_layout, anchor_x="center", anchor_y="bottom", align_y=40)
        self.letters_layout.visible = False

        # Inicjalizacja zmiennych gry
        self.guessed_letters = set()
        self.errors = 0

    def start_game_with_word(self, word):
        print(f"Start gry ze słowem: {word.word}")
        self.current_word = word.word.lower()
        self.sub_menu.visible = False
        self.visible = True
        self.letters_layout.visible = True

        self.masked_word = "_" * len(self.current_word)
        self.word_label.text = " ".join(self.masked_word)

        # Reset stanu gry
        self.guessed_letters.clear()
        self.errors = 0
        self.message_label.text = ""

        # Włącz wszystkie przyciski
        for button in self.letter_buttons:
            button.disabled = False

        self.is_running = True

    def on_letter_click(self, letter):
        letter_lower = letter.lower()
        if letter_lower in self.guessed_letters:
            return

        self.guessed_letters.add(letter_lower)

        for button in self.letter_buttons:
            if button.text == letter:
                button.disabled = True
                break

        if letter_lower in self.current_word:
            print(f"Litera '{letter}' jest w słowie!")
            self.update_display()
            if "_" not in self.masked_word:
                self.message_label.text = "Wygrałeś!!!"
                add_win_to_user(self.window.user_one.id)
                for button in self.letter_buttons:
                    button.disabled = True
        else:
            self.errors += 1
            print(f"Litera '{letter}' nie ma w słowie! Błędów: {self.errors}/{self.MAX_ERRORS}")
            if self.errors >= self.MAX_ERRORS:
                self.message_label.text = "Przegrałeś! Przekroczono maksymalną liczbę błędów."
                add_lose_to_user(self.window.user_one.id)
                for button in self.letter_buttons:
                    button.disabled = True
                self.word_label.text = " ".join(self.current_word.upper())

    def update_display(self):
        display_word = [letter if letter in self.guessed_letters else "_" for letter in self.current_word]
        self.masked_word = "".join(display_word)
        self.word_label.text = " ".join(display_word)

    def draw_hangman(self):
        base_x = 500
        base_y = 400

        arcade.draw_line(base_x, base_y, base_x + 150, base_y, arcade.color.BLACK, 5)
        arcade.draw_line(base_x + 70, base_y, base_x + 70, base_y + 250, arcade.color.BLACK, 5)
        arcade.draw_line(base_x + 70, base_y + 250, base_x + 150, base_y + 250, arcade.color.BLACK, 5)
        arcade.draw_line(base_x + 150, base_y + 250, base_x + 150, base_y + 230, arcade.color.BLACK, 5)

        head_x = base_x + 150
        head_y = base_y + 210

        if self.errors >= 1:
            arcade.draw_circle_outline(head_x, head_y, 25, arcade.color.BLACK, 5)
        if self.errors >= 2:
            arcade.draw_line(head_x, head_y - 25, head_x, head_y - 110, arcade.color.BLACK, 5)
        if self.errors >= 3:
            arcade.draw_line(head_x, head_y - 40, head_x - 35, head_y - 70, arcade.color.BLACK, 5)
        if self.errors >= 4:
            arcade.draw_line(head_x, head_y - 40, head_x + 35, head_y - 70, arcade.color.BLACK, 5)
        if self.errors >= 5:
            arcade.draw_line(head_x, head_y - 110, head_x - 30, head_y - 160, arcade.color.BLACK, 5)
        if self.errors >= 6:
            arcade.draw_line(head_x, head_y - 110, head_x + 30, head_y - 160, arcade.color.BLACK, 5)

    def on_draw(self):
        super().on_draw()
        if self.is_running and not self.sub_menu.visible:
            self.draw_hangman()

    def on_show_view(self):
        super().on_show_view()
        self.reset_game()

    def reset_game(self):
        self.current_word = ""
        self.masked_word = ""
        self.guessed_letters.clear()
        self.errors = 0
        self.word_label.text = ""
        self.message_label.text = ""
        self.letters_layout.visible = False

        # Dezaktywuj wszystkie przyciski
        for button in self.letter_buttons:
            button.disabled = True

        self.sub_menu.visible = True
        self.is_running = False
        self.start_time = None

    def __del__(self):
        print("GameView został usunięty z pamięci.")



class GameViewOnTime(GameView):
    def __init__(self, back_view, on_time: bool):
        super().__init__(back_view, on_time)
        if on_time:
            self.start_time = None
            self.elapsed_time = 0
            self.timer_label = UILabel(text="", font_size=24, text_color=arcade.color.RED, width=600)
            self.anchor.add(child=self.timer_label, anchor_x="left", anchor_y="top", align_y=-100)

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.start_time and self.is_running:
            current_time = time.time() - self.start_time
            self.elapsed_time = min(60, int(current_time))  # ograniczenie do 60 sekund
            self.timer_label.text = f"Czas: {self.elapsed_time}"

            # Sprawdzanie czy minęło 60 sekund
            if current_time >= 60 and self.message_label.text == "":
                self.message_label.text = "Przegrałeś! Koniec czasu!"
                add_lose_to_user(self.window.user_one.id)
                self.word_label.text = " ".join(self.current_word.upper())
                # Wyłączanie wszystkich przycisków
                for button in self.letter_buttons:
                    button.disabled = True
        else:
            self.timer_label.text = ""

    def reset_game(self):
        super().reset_game()
        self.timer_label.text = ""

    def start_game_with_word(self, word):
        print(f"Start gry ze słowem: {word.word}")
        self.current_word = word.word.lower()
        self.current_word_obj = word
        # Przechowujemy nazwę kategorii jako string zamiast próbować uzyskać dostęp do relacji
        self.current_category = getattr(word, '_category_name', None)  # używamy zapisanej nazwy kategorii
        self.sub_menu.visible = False
        self.visible = True
        super().start_game_with_word(word)

    def on_letter_click(self, letter):
        letter_lower = letter.lower()
        if letter_lower in self.guessed_letters:
            return

        self.guessed_letters.add(letter_lower)

        # Wyłącz przycisk
        for button in self.letter_buttons:
            if button.text == letter:
                button.disabled = True
                break

        if letter_lower in self.current_word:
            print(f"Litera '{letter}' jest w słowie!")
            self.update_display()
            if "_" not in self.masked_word:
                if self.on_time:
                    # Użyj zapisanej kategorii
                    new_word = get_random_word_from_category(self.current_category)
                    if new_word:
                        add_win_to_user(self.window.user_one.id)
                        self.guessed_letters.clear()
                        for btn in self.letter_buttons:
                            btn.disabled = False
                        self.start_game_with_word(new_word)
                else:
                    self.message_label.text = "Wygrałeś!!!"
                    add_win_to_user(self.window.user_one.id)
                    for button in self.letter_buttons:
                        button.disabled = True

        else:
            self.errors += 1
            print(f"Litera '{letter}' nie ma w słowie! Błędów: {self.errors}/{self.MAX_ERRORS}")

            if self.errors >= self.MAX_ERRORS:
                self.message_label.text = "Przegrałeś! Przekroczono maksymalną liczbę błędów."
                add_lose_to_user(self.window.user_one.id)
                for button in self.letter_buttons:
                    button.disabled = True
                self.word_label.text = " ".join(self.current_word.upper())