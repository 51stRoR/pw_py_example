import logging
import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


class TestLogin:

    @pytest.fixture(autouse=True)
    def setup_data(self, load_test_data, browser: Browser):
        self.base_url = load_test_data['base_url']
        test_users = load_test_data['test_users']
        self.standard_user_data = test_users['standard']
        self.locked_user_data = test_users['locked']
        self.context = browser.new_context()

    def test_login(self):
        page = self.context.new_page()
        login_page = LoginPage(page, self.base_url)
        login_page.navigate(login_page.url)
        login_page.login_user(self.standard_user_data['username'], self.standard_user_data['password'])
        inventory_page = InventoryPage(page, self.base_url)
        expect(inventory_page.inventory_container).to_be_visible()
        assert inventory_page.secondary_header.text_content() == "Products"
        assert inventory_page.url == page.url

    def test_login_locked(self):
        page = self.context.new_page()
        login_page = LoginPage(page, self.base_url)
        login_page.navigate(login_page.url)
        login_page.login_user(self.locked_user_data['username'], self.locked_user_data['password'])
        expect(login_page.locked_user_error_msg).to_be_visible()
        assert login_page.locked_user_error_msg.text_content() == "Epic sadface: Sorry, this user has been locked out."
        assert login_page.url == page.url
