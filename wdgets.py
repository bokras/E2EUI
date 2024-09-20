from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.label import Label

class MyBox(BoxLayout):
    button_arg = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.orientation = "horizontal"
        self.spacing = "5dp"
        self.size_hint_y = None

def Item(img_url="", title="", description="", price="",button_arg="", on_press=None, size=(100, 400)):
    layout = MyBox()
    layout.orientation = "horizontal"
    layout.spacing = "5dp"
    layout.size_hint_y = None
    layout.size = size

    if img_url[0] == "h":
        image = AsyncImage(source=img_url)
        layout.add_widget(image)

    elif img_url:
        image = Label()
        image.text = img_url
        layout.add_widget(image)

    title_label = Label()
    title_label.text = "Title:\n" + title
    layout.add_widget(title_label)

    if description:
        description_label = Label()
        description_label.size_hint = (1, .8)
        description_label.text = "Description:\n" + description.replace(",",",\n")
        description_label.font_size = description_label.width / 10
        description_label.pos_hint = {'center_x':0,'center_y':0.5}
        layout.add_widget(description_label)

    price_label = Label()
    price_label.text = "Price:\n" + price
    layout.add_widget(price_label)

    if button_arg:
        button = Button(text="Выбрать")
        button.bind(on_press=on_press)
        layout.button_arg = button_arg
        button.size_hint_y = .3
        button.size_hint_x = .3
        button.pos_hint = {'center_x':.5,'center_y':.5}
        layout.add_widget(button)
    return layout


