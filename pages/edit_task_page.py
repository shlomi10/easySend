from playwright.sync_api import Page
import allure
import logging

from pages.base_page import BasePage

log = logging.getLogger(__name__)


class EditTaskPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.dialog = page.locator("div[role='dialog']")
        self.name_input = self.dialog.locator("input[name='name']")
        self.description_textarea = self.dialog.locator("textarea[name='description']")
        self.deadline_input = self.dialog.locator("input[type='datetime-local']")
        self.category_dropdown = self.dialog.locator("div[role='combobox']")
        self.color_accordion = self.dialog.locator("button.MuiAccordionSummary-root")
        self.color_buttons = self.dialog.locator("button[id^='color-element-']")
        self.close_button = self.dialog.locator("button >> nth=0")
        self.cancel_button = self.dialog.locator("button:has-text('Cancel')")
        self.save_button = self.dialog.locator("button:has-text('Save')")

    @allure.step("Wait for Edit Task dialog to be visible")
    def wait_for_ready(self):
        self.wait_for_element_to_be_visible_and_clickable(self.name_input)
        self.wait_for_element_to_be_visible_locator(self.save_button)

    @allure.step("Edit task with name: {name}")
    def edit_task(self, name: str, description: str = None, deadline: str = None):
        self.wait_for_ready()
        self.name_input.fill(name)
        if description is not None:
            self.description_textarea.fill(description)
        if deadline is not None:
            self.deadline_input.fill(deadline)
        self.save_button.click()

    @allure.step("Close edit dialog")
    def close_dialog(self):
        self.click(self.close_button)

    @allure.step("Cancel editing")
    def cancel_edit(self):
        self.click(self.cancel_button)

    @allure.step("Select category")
    def select_category(self):
        self.click(self.category_dropdown)

    @allure.step("Toggle color picker")
    def open_color_picker(self):
        self.click(self.color_accordion)

    @allure.step("Pick color by index {index}")
    def pick_color(self, index: int):
        self.color_buttons.nth(index).click()
