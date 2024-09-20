import traceback
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger
from kivy.lang.builder import Builder
from kivy.config import Config
from kivy.core.window import Window
import windows


Builder.load_file("ui.kv")
wm = None


class E2E_UIApp(App):
    def build(self):
        global wm
        wm = ScreenManager()
        wm.add_widget(windows.SignIn(name="signin"))
        wm.add_widget(windows.ItemsScreen(name="items"))
        wm.add_widget(windows.OrderData(name="order"))
        wm.add_widget(windows.OrderStatus(name="status"))
        windows.set_wm(wm)
        return wm


def main():
    app = E2E_UIApp()
    app.run()

if __name__ == '__main__':
    main()


