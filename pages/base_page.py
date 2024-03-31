import logging
from playwright.sync_api import Page, Locator


logger = logging.getLogger(__name__)
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

class BasePage:

    def __init__(self, page: Page) -> None:
        self.page = page
    
    def navigate(self, url: str):
        logger.info(f"navigate to {url}")
        self.page.goto(url)
    
    def enter_text(self, element: Locator, text: str):
        element.clear()
        element.fill(text)
    
    def wait_for_url(self, url: str):
        logger.info(f"waiting for page to load: {url}")
        self.page.wait_for_url(url)
    
