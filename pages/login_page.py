import logging
from playwright.sync_api import Page
from pages.base_page import BasePage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class LoginPage(BasePage):
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    LOCKED_USER_ERROR = "//div[@class='error-message-container error']"

    def __init__(self, page: Page, base_url=None) -> None:
        self.page = page
        self.url = base_url if base_url else self.BASE_URL
        self.username = self.page.locator(self.USERNAME)
        self.password = self.page.locator(self.PASSWORD)
        self.login = self.page.locator(self.LOGIN_BTN)
        self.locked_user_error_msg = self.page.locator(self.LOCKED_USER_ERROR)
    
    def login_user(self, username: str, password: str):
        logger.info(f"enter username: {username}")
        self.enter_text(self.username, username)
        logger.info(f"enter password: {password}")
        self.enter_text(self.password, password)
        logger.info("click login button")
        self.login.click()
    


