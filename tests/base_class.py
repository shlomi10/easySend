import os

from dotenv import load_dotenv

from pages.add_task_page import AddTaskPage
from pages.edit_task_page import EditTaskPage
from pages.todo_page import TodoPage

dot_env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils", ".env"))
load_dotenv(dotenv_path=dot_env_path)

class BaseClass:
    def __init__(self, page):
        self.page = page
        self.base_url = os.getenv("BASE_URL")
        self.todo_page = TodoPage(self.page)
        self.add_task_page = AddTaskPage(self.page)
        self.edit_task_page = EditTaskPage(self.page)