import logging
import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class TestCart:

    @pytest.fixture(autouse=True)
    def setup_data(self, load_test_data):
        self.standard_user_data = load_test_data['test_users']['standard']
        self.test_items = load_test_data['test_items']

    def test_add_products_from_grid(self, browser: Browser):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_grid_page = InventoryPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(self.standard_user_data['username'], self.standard_user_data['password'])
        expect(product_grid_page.header).to_be_visible()
        product_grid_page.add_product_by_name(self.test_items[0]['name'])
        assert product_grid_page.delete_button.is_visible()
        assert product_grid_page.delete_button.text_content() == "Remove"
        assert product_grid_page.cart_badge.is_visible()
        assert product_grid_page.cart_badge.text_content() == "1"
        product_grid_page.add_product_by_name(self.test_items[1]['name'])
        assert product_grid_page.delete_button.is_visible()
        assert product_grid_page.delete_button.text_content() == "Remove"
        assert product_grid_page.cart_badge.is_visible()
        assert product_grid_page.cart_badge.text_content() == "2"

    def test_add_product(self, browser: Browser):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_grid_page = InventoryPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(self.standard_user_data['username'], self.standard_user_data['password'])
        expect(product_grid_page.header).to_be_visible()
        product_grid_page.go_to_product_page(self.test_items[0]['name'])
        product_page = ProductPage(page, self.test_items[0])
        expect(product_page.header).to_be_visible()
        assert product_page.product_title.text_content() == self.test_items[0]['name']
        assert product_page.product_description.text_content() == self.test_items[0]['description']
        assert product_page.product_price.text_content() == f"${self.test_items[0]['price']}"
        product_page.add_product()
        assert product_page.delete_button.is_visible()
        assert product_page.delete_button.text_content() == "Remove"
        assert product_page.cart_badge.is_visible()
        assert product_page.cart_badge.text_content() == "1"
    
    def test_cart_page(self, browser: Browser):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_grid_page = InventoryPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(self.standard_user_data['username'], self.standard_user_data['password'])
        expect(product_grid_page.header).to_be_visible()
        product_grid_page.add_product_by_name(self.test_items[0]['name'])
        product_grid_page.add_product_by_name(self.test_items[1]['name'])
        product_grid_page.cart_icon.click()
        cart_page = CartPage(page)
        expect(cart_page.header).to_be_visible()
        assert cart_page.checkout_btn.is_visible()
        assert cart_page.continue_btn.is_visible()
        for product in self.test_items:
            cart_page.get_data_by_product(product, self.test_items.index(product))
            assert cart_page.product_qty.text_content() == '1'
            assert cart_page.product_title.text_content() == product['name']
            assert cart_page.product_description.text_content() == product['description']
            assert cart_page.product_price.text_content() == f"${product['price']}"
            assert cart_page.remove_btn.is_visible()
