import logging
from playwright.sync_api import Page, Locator
from pages.base_page import HeaderPage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class InventoryPage(HeaderPage):
    URL = "inventory.html"
    ADD_CART_BTN = "#add-to-cart-{}"
    REMOVE_CART_BTN = "#remove-{}"
    PRODUCT_TITLE = "//div[@data-test='inventory-item-name' and text()='{}']"

    def __init__(self, page: Page, base_url=None) -> None:
        super().__init__(page, base_url)
    
    def add_product_by_name(self, product_name: str):
        name_id = product_name.replace(' ','-').lower()
        self.add_button = self.page.locator(self.ADD_CART_BTN.format(name_id))
        self.add_button.click()
        self.delete_button = self.page.locator(self.REMOVE_CART_BTN.format(name_id))
        self.cart_badge = self.page.locator(self.CART_BADGE)
    
    def go_to_product_page(self, product_name: str):
        self.product_title = self.page.locator(self.PRODUCT_TITLE.format(product_name))
        self.product_title.click()

