from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductPage(BasePage):
    HEADER = "#header_container"
    SECONDARY_HEADER = "//div[@class='header_secondary_container']/span"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = self.page.locator(self.HEADER)
        self.secondary_header = self.page.locator(self.SECONDARY_HEADER)

