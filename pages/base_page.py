import logging
from playwright.sync_api import Page, Locator


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class BasePage:
    BASE_URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page) -> None:
        self.page = page
    
    def navigate(self, url: str):
        logger.info(f"navigate to {url}")
        self.page.goto(url)
    
    def enter_text(self, element: Locator, text: str):
        element.clear()
        element.fill(text)
    
    def wait_for_url(self, url: str):
        logger.info(f"waiting for page to load: {url}")
        self.page.wait_for_url(url)


class HeaderPage(BasePage):
    URL = ""
    CART_BADGE = ".shopping_cart_badge"
    CART_ICON = ".shopping_cart_link"
    HEADER = "#header_container"
    SECONDARY_HEADER = "//div[data-test='secondary-header']/span"
    SIDEBAR_MENU = "#react-burger-menu-btn"
    ABOUT_LINK = "#about_sidebar_link"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page, base_url=None) -> None:
        self.page = page
        self.url = f"{base_url}{self.URL}" if base_url else f"{self.BASE_URL}{self.URL}"
        self.header = self.page.locator(self.HEADER)
        self.secondary_header = self.page.locator(self.SECONDARY_HEADER)
        self.sidebar_menu = self.page.locator(self.SIDEBAR_MENU)
        self.about_link = self.page.locator(self.ABOUT_LINK)
        self.logout_link = self.page.locator(self.LOGOUT_LINK)
        self.cart_icon = self.page.locator(self.CART_ICON)
    
    def select_menu_option(self, option: Locator):
        self.sidebar_menu.click()
        option.click()
