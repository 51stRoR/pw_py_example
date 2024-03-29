import logging
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class ProductGridPage(BasePage):
    HEADER = "#header_container"
    SECONDARY_HEADER = "//div[@class='header_secondary_container']/span"
    SIDEBAR_MENU = "#react-burger-menu-btn"
    ABOUT_LINK = "#about_sidebar_link"
    ADD_CART_BTN = "#add-to-cart-{}"
    REMOVE_CARD_BTN = "#remove-{}"
    CART_BADGE = '.shopping_cart_badge'
    PRODUCT_TITLE = "//div[@data-test='inventory-item-name' and text()='{}']"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = self.page.locator(self.HEADER)
        self.secondary_header = self.page.locator(self.SECONDARY_HEADER)
        self.sidebar_menu = self.page.locator(self.SIDEBAR_MENU)
        self.about_link = self.page.locator(self.ABOUT_LINK)
    
    def select_menu_option(self, option: Locator):
        self.sidebar_menu.click()
        option.click()
    
    def add_product_by_name(self, product_name: str):
        name_id = product_name.replace(' ','-').lower()
        self.add_button = self.page.locator(self.ADD_CART_BTN.format(name_id))
        self.add_button.click()
        self.delete_button = self.page.locator(self.REMOVE_CARD_BTN.format(name_id))
        self.cart_badge = self.page.locator(self.CART_BADGE)
    
    def go_to_product_page(self, product_name: str):
        self.product_title = self.page.locator(self.PRODUCT_TITLE.format(product_name))
        self.product_title.click()

