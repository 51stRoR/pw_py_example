import logging
from playwright.sync_api import Page
from pages.base_page import BasePage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class CheckoutPage(BasePage):
    URL = "/checkout-step-one.html"
    URL_UPD = "/checkout-step-two.html"
    HEADER = "#header_container"
    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    POSTAL_CODE = "#postal-code"
    PRODUCT_QTY = "//div[@data-test='item-quantity']"
    PRODUCT_TITLE = "//div[@data-test='inventory-item-name' and text()='{}']"
    PRODUCT_DESCRIPTION = "//div[@data-test='inventory-item-desc']"
    PRODUCT_PRICE = "//div[@data-test='inventory-item-price']"
    SHIPPING_INFO = "//div[@data-test='shipping-info-value']"
    TOTAL_ITEM_PRICE = "//div[@data-test='subtotal-label']"
    TOTAL_PRICE = "//div[@data-test='total-label']"
    TAX = "//div[@data-test='tax-label']"
    CART_BADGE = ".shopping_cart_badge"
    CART_ICON = ".shopping_cart_link"
    CONTINUE_BTN = "#continue"
    CANCEL_BTN = "#cancel"
    FINISH_BTN = "#finish"

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.url = f"{base_url}{self.URL}" if base_url else f"{self.BASE_URL}{self.URL}"
        self.url_upd = f"{base_url}{self.URL_UPD}" if base_url else f"{self.BASE_URL}{self.URL_UPD}"
        self.header = self.page.locator(self.HEADER)
        self.continue_btn = self.page.locator(self.CONTINUE_BTN)
        self.cancel_btn = self.page.locator(self.CANCEL_BTN)
        self.first_name = self.page.locator(self.FIRST_NAME)
        self.last_name = self.page.locator(self.LAST_NAME)
        self.postal_code = self.page.locator(self.POSTAL_CODE)
    
    def fill_user_info(self, fisrtname: str, lastname: str, postal_code: str):
        self.enter_text(self.first_name, fisrtname)
        self.enter_text(self.last_name, lastname)
        self.enter_text(self.postal_code, postal_code)
    
    def continue_checkout(self):
        self.continue_btn.click()
        self.url = self.url_upd
        self.finish_btn = self.page.locator(self.FINISH_BTN)
        self.shipping_info = self.page.locator(self.SHIPPING_INFO)
        self.total_item_price_label = self.page.locator(self.TOTAL_ITEM_PRICE)
        self.total_price_label = self.page.locator(self.TOTAL_PRICE)
        self.total_tax_label = self.page.locator(self.TAX)
    
    def get_data_by_product(self, product, index):
        self.product_qty = self.page.locator(self.PRODUCT_QTY).nth(index)
        self.product_title = self.page.locator(self.PRODUCT_TITLE.format(product['name']))
        self.product_price = self.page.locator(self.PRODUCT_PRICE).nth(index)
        self.product_description = self.page.locator(self.PRODUCT_DESCRIPTION).nth(index)
    
    def calculate_total_price(self):
        self.item_price = 0.0
        product_prices = self.page.locator(self.PRODUCT_PRICE).all()
        for p in product_prices:
            price = float(p.text_content().replace('$', ''))
            self.item_price += price
        self.tax_price = self.item_price * 0.08
        self.total_price = self.tax_price + self.item_price



class CheckoutCompletePage(BasePage):
    URL = "/checkout-complete.html"
    COMPLETE_HEADER = "//h2[@data-test='complete-header']"
    COMPLETE_TEXT = "//div[@data-test='complete-text']"
    BACK_BTN = "#back-to-products"

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.url = f"{base_url}{self.URL}" if base_url else f"{self.BASE_URL}{self.URL}"
        self.complete_header = self.page.locator(self.COMPLETE_HEADER)
        self.complete_text = self.page.locator(self.COMPLETE_TEXT)
        self.back_btn = self.page.locator(self.BACK_BTN)
