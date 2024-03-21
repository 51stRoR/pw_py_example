import pytest
from playwright.sync_api import Page, Browser, expect
from pages.login_page import LoginPage
from pages.product_page import ProductPage


class TestLogin:

    def test_login(self, browser: Browser):
        page = browser.new_page()
        login_page = LoginPage(page)
        product_page = ProductPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user("standard_user", "secret_sauce")
        expect(product_page.header).to_be_visible()
        assert product_page.get_text(product_page.secondary_header) == "Products"

    def test_login_locked(self, browser: Browser):
        page = browser.new_page()
        login_page = LoginPage(page)
        login_page.navigate(login_page.URL)
        login_page.login_user("locked_out_user", "secret_sauce")
        expect(login_page.locked_user_error_msg).to_be_visible()
        assert login_page.get_text(login_page.locked_user_error_msg) == "Epic sadface: Sorry, this user has been locked out."

