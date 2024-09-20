import platform
import time
import chromedriver_autoinstaller
import os
import traceback
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium_stealth import stealth
import elements_data as find_data



class WebTool:


    def __init__(self, hide=False):
        self.driver = None
        self.__wait = 20
        self.__hide = hide
        self.__exec_path = uc.find_chrome_executable()
        self.__login = ""
        self.__password = ""
        self.selection_name = ""
        self.btn_id = ""
        self.first_name = ""
        self.last_name = ""
        self.zip_code = ""
        self.items = []



    def __del__(self):
        self.close_driver()

    def __get_driver_path(self):
        if "windows" in platform.platform().lower():
            file = "chromedriver.exe"
        else:
            file = "chromedriver"
        chromedriver_folder = os.path.dirname(__file__)
        chromedriver_path = os.path.join(chromedriver_folder,file)
        if os.path.exists(chromedriver_path):
            return chromedriver_path
        chromedriver_path = chromedriver_autoinstaller.install(path=chromedriver_folder)
        return chromedriver_path

    def __create_driver(self):
        if self.driver:
            return
        print("инициализация драйвера...")
        options = uc.ChromeOptions()
        options.add_argument("start-maximized")
        if self.__hide:
            options.add_argument("--headless")
        try:
            driver_path = self.__get_driver_path()
            if driver_path:
                self.driver = uc.Chrome(browser_executable_path=self.__exec_path,
                                        driver_executable_path=driver_path, options=options)
                stealth(self.driver,
                        languages=["en-US", "en"],
                        vendor="Google Inc.",
                        platform="Win32",
                        webgl_vendor="Intel Inc.",
                        renderer="Intel Iris OpenGL Engine",
                        fix_hairline=True,
                        )
        except:
            print("ошибка инициализации")
            traceback.print_exc()


    def close_driver(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()
            self.driver = None


    def __get_and_wait_element(self, by:By, value:str) -> WebElement|None:
        wait = self.__wait
        element = None
        while not element:
            try:
                element = self.driver.find_element(by=by, value=value)
            except:
                wait -= 1
                if wait <= 0:
                    break
                time.sleep(1)
        return element


    def login_site(self, login:str="", password:str=""):
        try:
            if login:
                self.__login = login
                if password:
                    self.__password = password
            self.__create_driver()
            print("загрузка страницы...")
            self.driver.get("https://www.saucedemo.com/")
            login_input = self.__get_and_wait_element(By.CSS_SELECTOR, find_data.LOGIN_INPUT_CSS_SELECTOR)
            password_input = self.driver.find_element(By.CSS_SELECTOR, find_data.PASSWORD_INPUT_CSS_SELECTOR)
            login_btn = self.driver.find_element(By.CSS_SELECTOR, find_data.LOGIN_BTN_CSS_SELECTOR)
            print("ввод  данных...")
            login_input.clear()
            login_input.send_keys(self.__login)
            password_input.clear()
            password_input.send_keys(self.__password)
            login_btn.click()
            print("авторизация...")
            items_table = self.__get_and_wait_element(By.CLASS_NAME, find_data.ITEMS_TABLE_CLASS_NAME)
            if items_table:
                print("авторизация прошла успешно")
                return True
            else:
                print("не удалось авторизоваться")
                return False
        except:
            traceback.print_exc()
            return False


    def get_items(self) -> list|None:
        if self.items:
            return self.items
        print("получение каталога")
        self.login_site()
        try:
            result = []
            table = self.__get_and_wait_element(By.CLASS_NAME, find_data.ITEMS_TABLE_CLASS_NAME)
            items = table.find_elements(By.CSS_SELECTOR, find_data.ITEM_DIV_CSS_SELECTOR)
            for item in items:
                item_divs = item.find_elements(By.TAG_NAME, "div")
                item_description = item_divs[1]
                item_img_div = item_divs[0]
                img_link_object = item_img_div.find_element(By.TAG_NAME, "a")
                img_object = img_link_object.find_element(By.TAG_NAME, "img")
                img_link = img_object.get_attribute("src")
                label_div = item_description.find_element(By.CLASS_NAME, find_data.ITEM_LABEL_CLASS_NAME)
                label_link = label_div.find_element(By.TAG_NAME, "a")
                description_div = label_div.find_elements(By.TAG_NAME, "div")[1]
                description = description_div.text
                label = label_link.find_element(By.CSS_SELECTOR, find_data.TITLE_TEXT_CSS_SELECTOR)
                title = label.text.strip()
                price_bar_div = item.find_element(By.CLASS_NAME, find_data.PRICE_BAR_DIV_CLASS_NAME)
                price_div = price_bar_div.find_element(By.TAG_NAME, "div")
                price = price_div.text.strip()
                button = price_bar_div.find_element(By.TAG_NAME, "button")
                button_id = button.get_attribute("id")
                item_info = {
                    "img_link": img_link,
                    "title": title,
                    "description": description,
                    "price": price,
                    "button": button_id
                }
                result.append(item_info)
            self.items = result
            return result
        except:
            print("При поиске что-то пошло не так")
            traceback.print_exc()
            return None


    def add_to_cart(self):
        self.__create_driver()
        self.login_site()
        print("добавление в корзину")
        try:
            item_btn = self.__get_and_wait_element(By.ID, self.btn_id)
            item_btn.click()
            print("проверка наличия товара в корзине")
            cart_btn = self.driver.find_element(By.CSS_SELECTOR, find_data.CART_CSS_SELECTOR)
            cart_btn.click()
            self.__get_and_wait_element(By.CLASS_NAME, find_data.CART_ITEM_CLASS_NAME)
            cards = self.driver.find_elements(By.CLASS_NAME, find_data.CART_ITEM_CLASS_NAME)
            for card in cards:
                item_label = card.find_elements(By.TAG_NAME, "div")[1]
                label_link = item_label.find_element(By.TAG_NAME, "a")
                link_text_object = label_link.find_element(By.TAG_NAME, "div")
                title = link_text_object.text.strip().lower()
                if title == self.selection_name.lower():
                    print("Товар добавлен в корзину")
                    return True
        except:
            traceback.print_exc()
            return False


    def pay(self):
        try:
            print("оформление заказа...")
            checkout = self.driver.find_element(By.CSS_SELECTOR, find_data.CHECKOUT_BTN_CSS_SELECTOR)
            checkout.click()
            first_name_input = self.__get_and_wait_element(By.CSS_SELECTOR, find_data.ORDER_FIRSTNAME_CSS_SELECTOR)
            last_name_input = self.driver.find_element(By.CSS_SELECTOR, find_data.ORDER_LASTNAME_CSS_SELECTOR)
            postalcode_input = self.driver.find_element(By.CSS_SELECTOR, find_data.ORDER_POSTCODE_CSS_SELECTOR)
            continue_btn = self.driver.find_element(By.CSS_SELECTOR, find_data.CONTINUE_BTN_CSS_SELECTOR)
            print("заполнение формы заказа")
            first_name_input.clear()
            first_name_input.send_keys(self.first_name)
            last_name_input.clear()
            last_name_input.send_keys(self.last_name)
            postalcode_input.clear()
            postalcode_input.send_keys(self.zip_code)
            continue_btn.click()
            print("Подтверждение заказа")
            finish_btn = self.__get_and_wait_element(By.CSS_SELECTOR, find_data.FINISH_BTN_CSS_SELECTOR)
            finish_btn.click()
            print("получение статуса заказа")
            status_object = self.__get_and_wait_element(By.CSS_SELECTOR, find_data.ORDER_STATUS_CSS_SELECTOR)
            result_text = status_object.text.strip()
            try:
                self.driver.close()
                self.driver.quit()
            except:
                pass
            print(result_text)
            return result_text
        except:
            return "Error, check your connection!"


def test():
    login = "standard_user"
    password = "secret_sauce"
    sauce = WebTool(hide=True)
    signin = sauce.login_site(login=login, password=password)
    if not signin:
        return
    items:list = sauce.get_items()
    sauce.close_driver()
    print(items)
    # if not items:
    #     return
    # print("Товары:")
    # for i, item in enumerate(items):
    #     row = f"{i}: {item['title']}  {item['price']}\n\n"
    #     print(row)
    # number_item = int(input("Введите номер товара: "))
    # first_name = input("Введите имя: ")
    # last_name = input("Введите фамилию: ")
    # postal_code = input("Введите почтовый индекс: ")
    # selected:dict = items[number_item]
    # selection_name = selected["title"]
    # item_btn = selected["button"]
    # cart = sauce.add_to_cart(item_btn, selection_name)
    # if not cart:
    #     return
    # sauce.pay(first_name=first_name, last_name=last_name, zip_code=postal_code)


if __name__ == "__main__":
    test()