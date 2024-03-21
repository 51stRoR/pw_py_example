from playwright.sync_api import Page, Locator

class BasePage:

    def __init__(self, page: Page) -> None:
        self.page = page
    
    def navigate(self, url: str):
        self.page.goto(url)
    
    def enter_text(self, element: Locator, text: str):
        element.clear()
        element.fill(text)
    
    def get_text(self, element: Locator):
        return element.text_content()
    
