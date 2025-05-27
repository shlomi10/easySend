from playwright.sync_api import Page, Locator, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click(self, element: Locator, force: bool = False):
        """Click an element (expects a Locator)."""
        element.click(timeout=1000, force=force)

    def fill(self, element: Locator, text: str):
        """Fill an input field (expects a Locator)."""
        element.fill(text)

    def get_text(self, element: Locator) -> str:
        """Get the text content of an element (expects a Locator)."""
        return element.inner_text()

    def wait_for(self, timeout: int = 1000):
        """Wait for a page"""
        self.page.wait_for_timeout(timeout=timeout)

    def wait_for_element_not_to_be_visible(self):
        self.wait_for(3000)
        expect(self.page.locator("text=Preparing app for offline use...")).not_to_be_visible()
        expect(self.page.locator("text=App is ready to work offline.")).not_to_be_visible()

    def wait_for_element_to_be_visible_locator(self, element: Locator, timeout: int = 5000):
        """Wait for an element to be visible (expects a locator)."""
        expect(element).to_be_visible(timeout=timeout)

    def wait_for_element_to_be_visible_and_clickable(self, element: Locator, timeout: int = 5000):
        """Wait for an element to be visible and clickable (expects a locator)."""
        expect(element).to_be_visible(timeout=timeout)
        expect(element).to_be_enabled(timeout=timeout)
