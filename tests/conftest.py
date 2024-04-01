import logging
import pytest
import yaml
from playwright.sync_api import sync_playwright


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

def pytest_addoption(parser):
    parser.addoption("--setup", default="setup.yaml", help="test data setup yaml")

@pytest.fixture(scope="class")
def load_test_data(request):
    filename = request.config.getoption("--setup")
    logger.info(f"loading yaml file with test data: {filename}")
    with open(filename, "r") as file:
        test_data = yaml.safe_load(file)
    return test_data

@pytest.fixture(scope="class")
def browser(request):
    browser_type = request.config.getoption("--browser")
    with sync_playwright() as p:
        match browser_type[0].lower():
            case 'chromium':
                logger.info(f"selected browser: {browser_type[0].lower()}")
                browser = p.chromium.launch(headless=False)
            case 'firefox':
                logger.info(f"selected browser: {browser_type[0].lower()}")
                browser = p.firefox.launch(headless=False)
            case 'webkit':
                logger.info(f"selected browser: {browser_type[0].lower()}")
                browser = p.webkit.launch(headless=False)
            case _:
                logger.info("no browser option provided, selected webkit by default")
                browser = p.webkit.launch(headless=False)
        
        yield browser
        
        browser.close()
