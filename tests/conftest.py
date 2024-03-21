import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def browser(request):
    browser_type = request.config.getoption("--browser")
    with sync_playwright() as p:
        match browser_type[0].lower():
            case 'chromium':
                browser = p.chromium.launch(headless=False)
            case 'firefox':
                browser = p.firefox.launch(headless=False)
            case 'webkit':
                browser = p.webkit.launch(headless=False)
            case _:
                raise ValueError("Invalid browser type. Please choose 'chromium', 'firefox', or 'webkit'.")
        
        yield browser
        
        browser.close()
