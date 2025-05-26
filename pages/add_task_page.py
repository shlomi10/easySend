from playwright.sync_api import Page, expect
import allure
import logging

from pages.base_page import BasePage

log = logging.getLogger(__name__)

class AddTaskPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.task_name_input = page.locator("input[placeholder='Enter task name']")
        self.task_description_textarea = page.locator("textarea[placeholder='Enter task description']")
        self.task_deadline_input = page.locator("input[placeholder='Enter deadline date']")
        self.category_dropdown = page.locator("div[role='combobox'][aria-haspopup='listbox']")
        self.create_task_button = page.locator("button[type='button']", has_text="Create Task")
        self.color_picker_toggle = page.locator("button.MuiAccordionSummary-root")
        self.color_buttons = page.locator("button[id^='color-element-']")
        self.sidebar_button = page.locator("button[aria-label='Sidebar']")
        self.back_to_main_tasks = page.locator("button[aria-label='menu']")
        self.validation_error_message = page.locator("p.MuiFormHelperText-root.Mui-error")
        self.name_validation_error = page.locator("p[id$='-helper-text'].Mui-error")

    @allure.step("Submit task with name: {text}")
    def submit_task(self, text: str):
        log.info(f"Filling task name: '{text}'")
        self.fill(self.task_name_input, text)
        log.info("Clicking Create Task button")
        self.click(self.create_task_button, force= True)

    @allure.step("Fill task name only: {text}")
    def fill_task_name_only(self, text: str):
        log.info(f"Filling task name field with: '{text}' (length: {len(text)} characters)")
        self.fill(self.task_name_input, text)

    @allure.step("Attempt to submit empty task")
    def submit_empty_task(self):
        log.info("Clicking Create Task with empty input")
        self.wait_for_element_to_be_visible_and_clickable(self.create_task_button)
        self.click(self.create_task_button, force=True)

    @allure.step("Navigate back to main tasks")
    def navigate_to_main_tasks(self):
        log.info("Navigate back to main tasks")
        self.wait_for_element_to_be_visible_and_clickable(self.back_to_main_tasks)
        self.click(self.back_to_main_tasks)

    @allure.step("Get validation error message for name field")
    def get_validation_error_message(self) -> str:
        self.wait_for_element_to_be_visible_locator(self.name_validation_error)
        return self.get_text(self.name_validation_error)


