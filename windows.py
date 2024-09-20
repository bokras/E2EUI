from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
import wdgets
from threading import Thread
from selenium_web_tool import WebTool

wm:ScreenManager|None = None
tool = WebTool(hide=True)



def set_wm(new_wm:ScreenManager):
    global wm
    wm = new_wm


class SignIn(Screen):


    def submit(self):
        login_input = self.ids.login_input
        password_input = self.ids.password_input
        submit_btn = self.ids.submit_btn
        login = login_input.text
        password = password_input.text
        if login and password:
            submit_btn.text = "Loading..."
            submit_btn.disabled = True
            self.signin(login, password)

    @mainthread
    def signin(self, login, password):
        header_label = self.ids.header_label
        submit_btn = self.ids.submit_btn
        sign_in = tool.login_site(login, password)
        tool.close_driver()
        if sign_in:
            submit_btn.text = "SignIn"
            submit_btn.disabled = False
            wm.current = "items"
        else:
            submit_btn.text = "SignIn"
            submit_btn.disabled = False
            header_label.text = "Incorrect account data:"




class ItemsScreen(Screen):

    def enter(self):
        scroll = self.ids.scroll
        load_label = self.ids.load_label
        scroll.bind(minimum_height=scroll.setter('height'))
        self.items = tool.get_items()
        tool.close_driver()
        print(self.items)
        if not self.items:
            wm.current = "signin"
            wm.current = "items"
            return
        scroll.remove_widget(load_label)

        for i,item in enumerate(self.items):
            item = wdgets.Item(button_arg=str(i), img_url=item["img_link"],
                               title=item["title"],price=item["price"],on_press=self.selected)
            scroll.add_widget(item)


    def selected(self, instance):
        global tool, wm
        item = instance.parent
        item_id = int(item.button_arg)
        items:list = tool.items
        selected:dict = items[item_id]
        tool.btn_id = selected["button"]
        tool.selection_name = selected["title"]
        wm.current = "order"




class OrderData(Screen):

    def submit(self):
        global tool, wm
        first_name_input = self.ids.first
        last_name_input = self.ids.last
        zip_code_input = self.ids.zip
        first_name = first_name_input.text
        last_name = last_name_input.text
        zip_code = zip_code_input.text

        if first_name and last_name and zip_code:
            tool.first_name = first_name
            tool.last_name = last_name
            tool.zip_code = zip_code
            wm.current = "status"




class OrderStatus(Screen):

    def enter(self):
        back_btn = self.ids.back_btn
        info = self.ids.info
        tool.add_to_cart()
        text = tool.pay()
        info.text = text
        back_btn.disabled = False


    def back(self):
        global wm
        tool.close_driver()
        wm.current = "signin"