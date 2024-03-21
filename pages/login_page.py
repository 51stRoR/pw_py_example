from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    LOCKED_USER_ERROR = "//div[@class='error-message-container error']"
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.username = self.page.locator(self.USERNAME)
        self.password = self.page.locator(self.PASSWORD)
        self.login = self.page.locator(self.LOGIN_BTN)
        self.locked_user_error_msg = self.page.locator(self.LOCKED_USER_ERROR)
    
    def login_user(self, username: str, password: str):
        self.enter_text(self.username, username)
        self.enter_text(self.password, password)
        self.login.click()
    


