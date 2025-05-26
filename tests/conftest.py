import allure
import pytest
import logging
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from tests.base_class import BaseClass

# Setup log directory and file
log_dir = Path(__file__).resolve().parent.parent / "ui_tests-logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / "test.log"

# Clear existing handlers and set up a custom file handler
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_handler)
logging.getLogger().setLevel(logging.INFO)


@pytest.fixture(scope="function", autouse=True)
def initialize(request):
    with sync_playwright() as playwright:
        # Use environment variable to control headless mode
        # Default to headless=True when running in Docker
        is_headless = os.getenv("HEADLESS", "false").lower() == "true"

        browser = playwright.chromium.launch(
            headless=is_headless,
            args=["--disable-blink-features=AutomationControlled"]
        )

        # Only set viewport to None if running headed mode
        context_options = {"locale": "en-us"}
        if not is_headless:
            context_options["no_viewport"] = True

        context = browser.new_context(**context_options)
        page = context.new_page()

        # Only maximize window if running in headed mode
        if not is_headless:
            page.evaluate("window.moveTo(0, 0); window.resizeTo(screen.availWidth, screen.availHeight);")
            window_size = page.evaluate("() => ({ width: window.innerWidth, height: window.innerHeight })")
            page.set_viewport_size(window_size)

        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        base_class = BaseClass(page)
        page.goto(base_class.base_url)
        yield base_class

        try:
            # Attach screenshot if test failed
            if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
                screenshots_path = Path("../screenshots")
                screenshots_path.mkdir(parents=True, exist_ok=True)
                screenshot_file = screenshots_path / f"{request.node.name}.png"
                page.screenshot(path=str(screenshot_file), full_page=True)
                with screenshot_file.open("rb") as img:
                    allure.attach(img.read(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        finally:
            context.tracing.stop(path="../trace/trace.zip")
            browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        item.rep_call = rep

        # Attach a log file to an Allure report
        if log_path.exists():
            with open(log_path, "r", encoding="utf-8") as log_file:
                allure.attach(
                    log_file.read(),
                    name=f"log_{item.name}",
                    attachment_type=allure.attachment_type.TEXT
                )