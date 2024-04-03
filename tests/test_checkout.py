import logging
import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutInformationPage, CheckoutOverviewPage, CheckoutCompletePage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class TestCart:

    @pytest.fixture(autouse=True)
    def setup_data(self, load_test_data, browser: Browser):
        self.base_url = load_test_data['base_url']
        self.test_items = load_test_data['test_items']
        self.standard_user_data = load_test_data['test_users']['standard']
        self.page = browser.new_page()

    def test_complete_checkout_and_logout(self):
        self.login_page = LoginPage(self.page, self.base_url)
        self.login_page.navigate(self.login_page.url)
        self.login_page.login_user(self.standard_user_data['username'], self.standard_user_data['password'])
        self.inventory_page = InventoryPage(self.page, self.base_url)
        expect(self.inventory_page.header).to_be_visible()
        self.inventory_page.add_product_by_name(self.test_items[0]['name'])
        assert self.inventory_page.delete_button.is_visible()
        assert self.inventory_page.delete_button.text_content() == "Remove"
        assert self.inventory_page.cart_badge.is_visible()
        assert self.inventory_page.cart_badge.text_content() == "1"
        self.inventory_page.add_product_by_name(self.test_items[1]['name'])
        assert self.inventory_page.delete_button.is_visible()
        assert self.inventory_page.delete_button.text_content() == "Remove"
        assert self.inventory_page.cart_badge.is_visible()
        assert self.inventory_page.cart_badge.text_content() == "2"
        self.inventory_page.go_to_product_page(self.test_items[2]['name'])
        self.product_page = ProductPage(self.page, self.test_items[2], self.base_url)
        expect(self.product_page.header).to_be_visible()
        assert self.product_page.add_to_cart.is_visible()
        assert self.product_page.product_title.text_content() == self.test_items[2]['name']
        assert self.product_page.product_description.text_content() == self.test_items[2]['description']
        assert self.product_page.product_price.text_content() == f"${self.test_items[2]['price']}"
        self.product_page.add_product()
        assert self.product_page.delete_button.is_visible()
        assert self.product_page.delete_button.text_content() == "Remove"
        assert self.product_page.cart_badge.is_visible()
        assert self.product_page.cart_badge.text_content() == "3"
        self.product_page = ProductPage(self.page, self.test_items[2], self.base_url)
        self.product_page.cart_icon.click()
        self.cart_page = CartPage(self.page, self.base_url)
        expect(self.cart_page.header).to_be_visible()
        assert self.cart_page.checkout_btn.is_visible()
        assert self.cart_page.continue_btn.is_visible()
        for product in self.test_items:
            self.cart_page.get_data_by_product(product, self.test_items.index(product))
            assert self.cart_page.product_qty.text_content() == '1'
            assert self.cart_page.product_title.text_content() == product['name']
            assert self.cart_page.product_description.text_content() == product['description']
            assert self.cart_page.product_price.text_content() == f"${product['price']}"
            assert self.cart_page.remove_btn.is_visible()
        
        self.cart_page.checkout_btn.click()
        self.checkout_page = CheckoutInformationPage(self.page, self.base_url)
        expect(self.checkout_page.header).to_be_visible()
        assert self.checkout_page.first_name.is_visible()
        assert self.checkout_page.last_name.is_visible()
        assert self.checkout_page.postal_code.is_visible()
        assert self.checkout_page.continue_btn.is_visible()
        self.checkout_page.fill_user_info(self.standard_user_data['first_name'], self.standard_user_data['last_name'], self.standard_user_data['zip'])
        self.checkout_page.continue_btn.click()
        self.checkout_overview_page = CheckoutOverviewPage(self.page, self.base_url)
        for product in self.test_items:
            self.checkout_overview_page.get_data_by_product(product, self.test_items.index(product))
            assert self.checkout_overview_page.product_qty.text_content() == '1'
            assert self.checkout_overview_page.product_title.text_content() == product['name']
            assert self.checkout_overview_page.product_description.text_content() == product['description']
            assert self.checkout_overview_page.product_price.text_content() == f"${product['price']}"
        self.checkout_overview_page.calculate_total_price()
        assert self.checkout_overview_page.total_item_price_label.text_content() == f"Item total: ${self.checkout_overview_page.item_price:.2f}"
        assert self.checkout_overview_page.total_tax_label.text_content() == f"Tax: ${self.checkout_overview_page.tax_price:.2f}"
        assert self.checkout_overview_page.total_price_label.text_content() == f"Total: ${self.checkout_overview_page.total_price:.2f}"
        assert self.checkout_overview_page.finish_btn.is_visible()
        self.checkout_overview_page.finish_btn.click()
        self.complete_page = CheckoutCompletePage(self.page, self.base_url)
        assert self.complete_page.complete_header.text_content() == "Thank you for your order!"
        assert self.complete_page.complete_text.text_content() == "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
        assert self.complete_page.back_btn.is_visible()
        self.complete_page.back_btn.click()
        expect(self.inventory_page.header).to_be_visible()
        self.inventory_page.select_menu_option(self.inventory_page.logout_link)
        self.login_page.wait_for_url(self.base_url)
        assert self.login_page.login_container.is_visible()
        assert self.login_page.login.is_visible()
        assert self.login_page.username.get_attribute('value') == ''
        assert self.login_page.password.get_attribute('value') == ''

