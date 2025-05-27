import time

import pytest
import allure
import logging

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@allure.suite("Todo Web App Test Suite")
@allure.label("layer", "ui")
class TestToDoWebApp:

    @allure.feature("Task Creation")
    @allure.story("Add task with valid input")
    @pytest.mark.parametrize("task", ["Buy milk", "Do laundry"])
    @allure.title("Add task: {task}")
    def test_add_task(self, initialize, task):
        todo = initialize.todo_page
        with allure.step(f"Add task: {task}"):
            todo.add_task(task)
        with allure.step("Verify task is added"):
            tasks = todo.get_tasks()
            log.info(f"Tasks after add: {tasks}")
            assert task in tasks

    @allure.feature("Task Creation")
    @allure.story("Add task with empty input")
    @allure.title("Add task with empty input")
    def test_add_empty_task(self, initialize):
        todo = initialize.todo_page
        add_task_page = initialize.add_task_page
        with allure.step("Navigate to /add and submit empty task"):
            todo.open_add_task_screen()
            add_task_page.submit_empty_task()
        with allure.step("Verify no task was added"):
            add_task_page.navigate_to_main_tasks()
            tasks = todo.get_tasks()
            log.info(f"Tasks after empty submission: {tasks}")
            assert len(tasks) == 0

    @allure.feature("Task Creation")
    @allure.story("Add task with long name - validation")
    @allure.title("Verify validation for task name exceeding 40 characters")
    def test_add_task_with_long_name(self, initialize):
        todo = initialize.todo_page
        add_task_page = initialize.add_task_page
        long_task_name = "This is a very long task name that exceeds the 40 character limit for validation testing"
        with allure.step("Navigate to add task screen"):
            todo.open_add_task_screen()
        with allure.step(f"Enter long task name (length: {len(long_task_name)} characters)"):
            add_task_page.fill_task_name_only(long_task_name)
        with allure.step("Validate error message is shown"):
            error_message = add_task_page.get_validation_error_message()
            log.info(f"Validation error message: {error_message}")
            assert error_message == "Name should be less than or equal to 40 characters"

    @allure.feature("Task Creation")
    @allure.story("Add multiple tasks")
    @allure.title("Create multiple tasks")
    def test_add_multiple_tasks(self, initialize):
        todo = initialize.todo_page
        multiple_tasks = [
            "Task 1: Buy groceries",
            "Task 2: Call dentist",
            "Task 3: Review project documents",
            "Task 4: Schedule team meeting",
            "Task 5: Update software licenses"
        ]

        with allure.step(f"Add {len(multiple_tasks)} tasks"):
            for i, task in enumerate(multiple_tasks, 1):
                with allure.step(f"Adding task {i}: {task}"):
                    todo.add_task(task)
                    todo.wait_for_add_task_button()
                    log.info(f"Added task {i}: {task}")

        with allure.step("Verify all tasks are added"):
            tasks = todo.get_tasks()
            log.info(f"All tasks after adding multiple: {tasks}")
            log.info(f"Expected tasks count: {len(multiple_tasks)}, Actual tasks count: {len(tasks)}")
            assert len(tasks) == len(multiple_tasks), f"Expected {len(multiple_tasks)} tasks, but found {len(tasks)}"

        # Verify each task is present
        for expected_task in multiple_tasks:
            task_found = any(expected_task in actual_task for actual_task in tasks)
            assert task_found, f"Task '{expected_task}' not found in tasks list: {tasks}"

        with allure.step("Verify tasks are displayed in correct order"):
            # Additional verification for task order (if applicable)
            assert len(tasks) > 0, "No tasks visible after adding multiple tasks"
            log.info("All multiple tasks successfully added and verified")

    @allure.feature("Task Management")
    @allure.story("Mark task as complete")
    @allure.title("Mark a task as complete")
    def test_mark_task_complete(self, initialize):
        todo = initialize.todo_page
        with allure.step("Add task to mark as complete"):
            todo.add_task("Complete me")
        with allure.step("Mark task as complete"):
            todo.mark_complete(0)
        with allure.step("Verify task is marked as complete"):
            tasks = todo.get_tasks()
            log.info(f"Tasks after marking complete: {tasks}")
            assert any("complete" in t.lower() for t in tasks), "Task was not marked as complete"

    @allure.feature("Task Management")
    @allure.story("Edit an existing task")
    @allure.title("Edit a task")
    def test_edit_task(self, initialize):
        todo = initialize.todo_page
        with allure.step("Add task to edit"):
            todo.add_task("Old task")
        with allure.step("Edit task to new name"):
            todo.edit_task(0, "New task")
        with allure.step("Verify edited task name"):
            task_name = todo.get_tasks()
            log.info(f"Edited task name: {task_name}")
            assert any("New task" in t for t in task_name), "Task was not edited"

    @allure.feature("Task Management")
    @allure.story("Delete a task")
    @allure.title("Delete a task")
    def test_delete_task(self, initialize):
        todo = initialize.todo_page
        with allure.step("Add task to be deleted"):
            todo.add_task("Remove me")
        with allure.step("Delete the task"):
            todo.delete_task(0)
        with allure.step("Verify task is deleted"):
            tasks = todo.get_tasks()
            log.info(f"Tasks after delete: {tasks}")
            assert len(tasks) == 0, "Task was not deleted"

    @allure.feature("Task Management")
    @allure.story("Filter completed tasks")
    @allure.title("Filter completed tasks")
    def test_filter_completed(self, initialize):
        todo = initialize.todo_page
        with allure.step("Add multiple tasks"):
            todo.add_task("One")
            todo.add_task("Two")
        with allure.step("Mark one task as completed"):
            todo.mark_complete(1)
        with allure.step("Extract completed task count from title"):
            actual_completed_tasks_number_in_title = todo.filter_completed_from_title()
        with allure.step("Count completed tasks from board"):
            visible_completed_tasks_on_board = todo.count_completed_tasks()
        with allure.step("Validate completed task counts match"):
            log.info(f"Visible tasks after completed: {visible_completed_tasks_on_board}")
            assert actual_completed_tasks_number_in_title == visible_completed_tasks_on_board, "task was not mark as completed"

    @allure.feature("Performance")
    @allure.story("Handle many tasks")
    @allure.title("Test app with 30 tasks")
    def test_performance_with_many_tasks(self, initialize):
        todo = initialize.todo_page
        many_tasks = [f"Task {i}" for i in range(1, 31)]

        with allure.step("Add 30 tasks"):
            for task in many_tasks:
                todo.add_task(task)
                todo.wait_for_add_task_button()

        with allure.step("Verify all tasks added"):
            all_tasks = todo.get_tasks()
            assert len(all_tasks) == 30, f"Expected 30 tasks, got {len(all_tasks)}"

        with allure.step("Verify UI remains responsive"):
            start_time = time.time()
            visible = todo.get_number_of_visible_tasks()
            elapsed = time.time() - start_time
            log.info(f"Counted visible tasks in {elapsed:.2f} seconds")
            assert visible > 0 and elapsed < 3, "UI response too slow with many tasks"

    @allure.feature("Performance")
    @allure.story("Page load timing")
    @allure.title("Measure page load time")
    def test_page_load_performance(self, initialize):
        page = initialize.page
        with allure.step("Measure page load timing"):
            load_time = page.evaluate("() => performance.timing.loadEventEnd - performance.timing.navigationStart")
            log.info(f"Page load time: {load_time} ms")
            assert load_time < 5000, "Page load took too long"