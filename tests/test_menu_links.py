import logging
import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class TestLinks:

    @pytest.fixture(autouse=True)
    def setup_data(self, load_test_data):
        self.about_link = load_test_data['links']['about_link']
        self.standard_user_data = load_test_data['test_users']['standard']
        self.locked_user_data = load_test_data['test_users']['locked']

    def test_about_link(self, browser: Browser):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_page = InventoryPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(self.standard_user_data['username'], self.standard_user_data['password'])
        expect(product_page.header).to_be_visible()
        product_page.select_menu_option(product_page.about_link)
        product_page.wait_for_url(self.about_link)
        assert page.url == self.about_link
        assert page.title() == "Sauce Labs: Cross Browser Testing, Selenium Testing & Mobile Testing"