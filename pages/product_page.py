from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class ProductPage(BasePage):
    HEADER = "#header_container"
    SECONDARY_HEADER = "//div[@class='header_secondary_container']/span"
    SIDEBAR_MENU = "#react-burger-menu-btn"
    ABOUT_LINK = "#about_sidebar_link"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = self.page.locator(self.HEADER)
        self.secondary_header = self.page.locator(self.SECONDARY_HEADER)
        self.sidebar_menu = self.page.locator(self.SIDEBAR_MENU)
        self.about_link = self.page.locator(self.ABOUT_LINK)
    
    def select_menu_option(self, option: Locator):
        self.sidebar_menu.click()
        option.click()
