import logging
from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class ProductPage(BasePage):
    URL = "/inventory-item.html?id={}"
    HEADER = "#inventory_item_container"
    ADD_CART_BTN = "#add-to-cart"
    REMOVE_CART_BTN = "#remove"
    CART_BADGE = '.shopping_cart_badge'
    CART_ICON = '.shopping_cart_link'
    PRODUCT_TITLE = "//div[@data-test='inventory-item-name' and text()='{}']"
    PRODUCT_DESCRIPTION = "//div[@data-test='inventory-item-desc']"
    PRODUCT_PRICE = "//div[@data-test='inventory-item-price']"

    def __init__(self, page: Page, product, base_url: str) -> None:
        self.page = page
        url = self.URL.format(product['id'])
        self.url = f"{base_url}{url}" if base_url else f"{self.BASE_URL}{url}"
        self.header = self.page.locator(self.HEADER)
        self.cart_icon = self.page.locator(self.CART_ICON)
        self.add_to_cart = self.page.locator(self.ADD_CART_BTN)
        self.product_title = self.page.locator(self.PRODUCT_TITLE.format(product['name']))
        self.product_price = self.page.locator(self.PRODUCT_PRICE)
        self.product_description = self.page.locator(self.PRODUCT_DESCRIPTION)


    def add_product(self):
        self.add_to_cart.click()
        self.delete_button = self.page.locator(self.REMOVE_CART_BTN)
        self.cart_badge = self.page.locator(self.CART_BADGE)
