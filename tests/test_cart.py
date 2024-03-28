import logging
import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.product_page import ProductPage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class TestCart:

    def test_add_product(self, browser: Browser, standard_user_data):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_page = ProductPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(standard_user_data['username'], standard_user_data['password'])
        expect(product_page.header).to_be_visible()
        product_page.add_product_by_name("Sauce Labs Bolt T-Shirt")
        assert product_page.delete_button.is_visible()
        assert product_page.get_text(product_page.delete_button) == "Remove"
        assert product_page.cart_badge.is_visible()
        assert product_page.get_text(product_page.cart_badge) == "1"
