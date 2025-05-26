from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.add_task_page import AddTaskPage
import allure
import logging

log = logging.getLogger(__name__)


class TodoPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.search_input = page.locator("input[placeholder='Search for task...']")
        self.sort_button = page.locator("button:has-text('Sort')")
        self.task_items = page.locator("[data-testid='task-container']")
        self.add_task_button = page.locator("button[aria-label='Add Task']")
        self.task_title = page.locator("[data-testid='task-container'] h3")
        self.task_timestamp = page.locator("[data-testid='task-container'] p")
        self.task_menu_button = page.locator("[aria-label='Task Menu']")
        self.task_menu_button_string = "[aria-label='Task Menu']"
        self.edit_input = page.locator("input[name='name']")
        self.create_task_btn = page.locator("button:has-text('Create Task')")
        self.edit_btn = page.locator("li:has-text('Edit')")
        self.save_button = page.locator("button:has-text('Save')")
        self.delete_btn = page.locator("li:has-text('Delete')")
        self.mark_as_done_btn = page.locator("li:has-text('Mark as done')")
        self.confirm_delete_btn = page.locator("button:has-text('Confirm Delete')")
        self.completed_info = page.locator("h4:has-text('You')")
        self.all_tasks = page.locator('[data-testid="task-container"]')

    @allure.step("Navigate to Add Task screen")
    def open_add_task_screen(self):
        self.click(self.add_task_button, force=True)
        return AddTaskPage(self.page)

    @allure.step("Add task through /add screen: {text}")
    def add_task(self, text: str):
        form = self.open_add_task_screen()
        form.submit_task(text)
        self.wait_for()

    @allure.step("wait for add task button to be visible")
    def wait_for_add_task_button(self):
        self.wait_for()
        self.wait_for_element_to_be_visible_and_clickable(self.add_task_button)

    @allure.step("Get current task titles")
    def get_tasks(self):
        return self.task_title.all_inner_texts()

    @allure.step("Mark task at index {index} as complete")
    def mark_complete(self, index: int):
        self.wait_for_element_to_be_visible_locator(self.task_items.nth(index))
        self.click(self.task_items.nth(index).locator(self.task_menu_button_string))
        self.click(self.mark_as_done_btn)

    @allure.step("Delete task at index {index}")
    def delete_task(self, index: int):
        self.click(self.task_items.nth(index).locator(self.task_menu_button_string))
        self.click(self.delete_btn)
        self.click(self.confirm_delete_btn)

    @allure.step("Edit task at index {index} to '{new_text}'")
    def edit_task(self, index: int, new_text: str):
        self.click(self.task_items.nth(index).locator(self.task_menu_button_string))
        self.click(self.edit_btn)
        self.fill(self.edit_input, new_text)
        self.click(self.save_button)

    @allure.step("Filter completed tasks from title")
    def filter_completed_from_title(self) -> int:
        text = self.completed_info.inner_text()
        return int(text.split("completed")[1].split("out")[0].strip())

    @allure.step("Get number of visible tasks")
    def get_number_of_visible_tasks(self) -> int:
        return sum(self.all_tasks.nth(i).is_visible() for i in range(self.all_tasks.count()))

    @allure.step("Count completed tasks (by check icon presence)")
    def count_completed_tasks(self) -> int:
        count = 0
        for i in range(self.all_tasks.count()):
            task = self.all_tasks.nth(i)
            if task.locator("span.css-d6pu1g").count() > 0:
                count += 1
        return count
