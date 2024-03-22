import logging
import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.product_page import ProductPage


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class TestLinks:

    def test_about_link(self, browser: Browser, standard_user_data):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_page = ProductPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user(standard_user_data['username'], standard_user_data['password'])
        expect(product_page.header).to_be_visible()
        product_page.select_menu_option(product_page.about_link)
        product_page.wait_for_url("https://saucelabs.com/")
        assert page.url == "https://saucelabs.com/"
        assert page.title() == "Sauce Labs: Cross Browser Testing, Selenium Testing & Mobile Testing"