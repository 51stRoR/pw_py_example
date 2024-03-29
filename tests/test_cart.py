import logging
import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.products_page import ProductGridPage
from pages.product_page import Productage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class TestCart:

    def test_add_products_from_grid(self, browser: Browser, standard_user_data):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_grid_page = ProductGridPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(standard_user_data['username'], standard_user_data['password'])
        expect(product_grid_page.header).to_be_visible()
        product_grid_page.add_product_by_name("Sauce Labs Bolt T-Shirt")
        assert product_grid_page.delete_button.is_visible()
        assert product_grid_page.get_text(product_grid_page.delete_button) == "Remove"
        assert product_grid_page.cart_badge.is_visible()
        assert product_grid_page.get_text(product_grid_page.cart_badge) == "1"
        product_grid_page.add_product_by_name("Sauce Labs Fleece Jacket")
        assert product_grid_page.delete_button.is_visible()
        assert product_grid_page.get_text(product_grid_page.delete_button) == "Remove"
        assert product_grid_page.cart_badge.is_visible()
        assert product_grid_page.get_text(product_grid_page.cart_badge) == "2"

    def test_add_product(self, browser: Browser, standard_user_data):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_grid_page = ProductGridPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(standard_user_data['username'], standard_user_data['password'])
        expect(product_grid_page.header).to_be_visible()
        product_grid_page.go_to_product_page("Sauce Labs Bolt T-Shirt")
        product_page = Productage(page)
        expect(product_page.header).to_be_visible()
        product_page.add_product()
        assert product_page.delete_button.is_visible()
        assert product_page.get_text(product_page.delete_button) == "Remove"
        assert product_page.cart_badge.is_visible()
        assert product_page.get_text(product_page.cart_badge) == "1"
