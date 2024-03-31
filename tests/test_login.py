import logging
import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.products_page import ProductGridPage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class TestLogin:

    @pytest.fixture(autouse=True)
    def setup_data(self, load_test_data):
        test_users = load_test_data['test_users']
        self.standard_user_data = test_users['standard']
        self.locked_user_data = test_users['locked']

    def test_login(self, browser: Browser):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_page = ProductGridPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(self.standard_user_data['username'], self.standard_user_data['password'])
        expect(product_page.header).to_be_visible()
        assert product_page.secondary_header.text_content() == "Products"

    def test_login_locked(self, browser: Browser):
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(self.locked_user_data['username'], self.locked_user_data['password'])
        expect(login_page.locked_user_error_msg).to_be_visible()
        assert login_page.locked_user_error_msg.text_content() == "Epic sadface: Sorry, this user has been locked out."

