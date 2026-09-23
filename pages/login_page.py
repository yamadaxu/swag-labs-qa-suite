"""登录页 Page Object。封装 Swag Labs 登录页的定位与操作。"""

URL = "https://www.saucedemo.com"


class LoginPage:
    def __init__(self, sb):
        self.sb = sb

    def open(self):
        self.sb.open(URL)
        return self

    def login(self, username, password, submit=True):
        self.sb.type("#user-name", username)
        self.sb.type("#password", password)
        if submit:
            self.sb.click('input[type="submit"]')
        return self

    def get_error_text(self):
        if self.sb.is_element_present("div.error-message-container.error"):
            return self.sb.get_text("div.error-message-container.error")
        return ""

    def has_error(self):
        return self.sb.is_element_present("div.error-message-container.error")

    def is_on_inventory(self):
        return self.sb.is_element_present("div.inventory_list")