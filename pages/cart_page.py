import logging
from playwright.sync_api import Page
from pages.base_page import BasePage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class CartPage(BasePage):
    URL = "/cart.html"
    HEADER = "#header_container"
    PRODUCT_QTY = "//div[@data-test='item-quantity']"
    PRODUCT_TITLE = "//div[@data-test='inventory-item-name' and text()='{}']"
    PRODUCT_DESCRIPTION = "//div[@data-test='inventory-item-desc']"
    PRODUCT_PRICE = "//div[@data-test='inventory-item-price']"
    REMOVE_CART_BTN = "#remove-{}"
    CONTINUE_BTN = "#continue-shopping"
    CHECKOUT_BTN = "#checkout"

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.url = f"{base_url}{self.URL}" if base_url else f"{self.BASE_URL}{self.URL}"
        self.header = self.page.locator(self.HEADER)
        self.checkout_btn = self.page.locator(self.CHECKOUT_BTN)
        self.continue_btn = self.page.locator(self.CONTINUE_BTN)
    
    def get_data_by_product(self, product, index):
        name_id = product['name'].replace(' ','-').lower()
        self.product_qty = self.page.locator(self.PRODUCT_QTY).nth(index)
        self.product_title = self.page.locator(self.PRODUCT_TITLE.format(product['name']))
        self.product_price = self.page.locator(self.PRODUCT_PRICE).nth(index)
        self.product_description = self.page.locator(self.PRODUCT_DESCRIPTION).nth(index)
        self.remove_btn = self.page.locator(self.REMOVE_CART_BTN.format(name_id))
    
    