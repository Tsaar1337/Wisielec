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
                print(f"Kliknięto kategorię: {name}")  # Możesz tu później odpalać inne akcje
                self.game_view.start_game_with_word(word)

            button_box.add(button)

        frame.add(button_box, anchor_x="center", anchor_y="center",align_y=-25)


class GameView(BaseView):

    def __init__(self, back_view):
        super().__init__(back_view)
        self.back_view = self.window.menu_game_view
        self.sub_menu = SubMenu(self)
        self.sub_menu.visible = True

        self.anchor.add(child=self.sub_menu, anchor_x="center", anchor_y="center")

        # Label do wyświetlania słowa wisielca
        self.word_label = UILabel(text="", font_size=36, text_color=arcade.color.BLACK, width=600, multiline=False)
        self.anchor.add(child=self.word_label, anchor_x="center", anchor_y="bottom", align_y=50)

        self.current_word = None
        self.masked_word = None


    def start_game_with_word(self, word):
            print(f"Start gry ze słowem: {word.word}")
            self.current_word = word.word.lower()
            self.sub_menu.visible = False

            # Utwórz maskę - same podkreślenia na początek
            self.masked_word = "_" * len(self.current_word)

            # Wyświetl maskę w labelu
            self.word_label.text = " ".join(self.masked_word)  # doda spacje między literami








