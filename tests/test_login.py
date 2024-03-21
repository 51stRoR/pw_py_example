import logging
import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.product_page import ProductPage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class TestLogin:

    def test_login(self, browser: Browser, standard_user_data):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_page = ProductPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(standard_user_data['username'], standard_user_data['password'])
        expect(product_page.header).to_be_visible()
        assert product_page.get_text(product_page.secondary_header) == "Products"

    def test_login_locked(self, browser: Browser, locked_user_data):
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(locked_user_data['username'], locked_user_data['password'])
        expect(login_page.locked_user_error_msg).to_be_visible()
        assert login_page.get_text(login_page.locked_user_error_msg) == "Epic sadface: Sorry, this user has been locked out."

