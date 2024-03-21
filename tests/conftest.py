import logging
import pytest
import yaml
from playwright.sync_api import sync_playwright


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

def pytest_addoption(parser):
    parser.addoption("--setup", default="setup.yaml", help="test data setup yaml")

def load_test_data(file_path):
    logger.info(f"loading yaml file with test data: {file_path}")
    with open(file_path, "r") as file:
        test_data = yaml.safe_load(file)
    return test_data.get("test_users", {})

@pytest.fixture(scope="class")
def standard_user_data(request):
    logger.info("Loading standard user data...")
    file_path = request.config.getoption("--setup")
    test_data = load_test_data(file_path).get("standard", {})
    logger.info(f"standard user data: {test_data}")
    return test_data

@pytest.fixture(scope="class")
def locked_user_data(request):
    logger.info("Loading locked user data...")
    file_path = request.config.getoption("--setup")
    test_data = load_test_data(file_path).get("locked", {})
    logger.info(f"locked user data: {test_data}")
    return test_data

@pytest.fixture(scope="function")
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
