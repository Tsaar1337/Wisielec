import arcade
from arcade.gui import UIFlatButton, UIManager, UIAnchorLayout, UILabel, UIBoxLayout, UIInputText, UIGridLayout, \
    UIMouseFilterMixin, NinePatchTexture

from UserInterface.view_utils import BaseView



class SubMenu(UIMouseFilterMixin, UIAnchorLayout):
    def __init__(self):
        super().__init__(size_hint=(1,1))
        font = "Comic Sans MS"

        frame = self.add(UIAnchorLayout(width=300, height=400, size_hint=None))
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

        category_label = UILabel(text="Wybierz kategorię", font_size=20, text_color=arcade.color.BLACK, width=200, font_name=font)

        anchor_label_in_frame = UIAnchorLayout()
        anchor_label_in_frame.add(category_label, anchor_x="center", anchor_y="top", align_y=20)

        frame.add(anchor_label_in_frame)




class GameView(BaseView):

    def __init__(self, back_view):
        super().__init__(back_view)
        self.back_view = self.window.menu_game_view
        self.sub_menu = SubMenu()

        self.anchor.add(child=self.sub_menu, anchor_x="center", anchor_y="center")
        # title_box = UIBoxLayout(vertical=True, space_between=20)
        # main_label = UILabel(text="Tu będzie gra", width=1000, text_color=arcade.color.BLACK, font_size=100,
        #                      font_name=self.font)
        # title_box.add(main_label)
        # self.anchor.add(
        #     child=title_box,
        #     anchor_x="center",
        #     anchor_y="top",
        #     align_y=-30
        # )






