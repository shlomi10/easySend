import allure
import pytest
import logging
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from tests.base_class import BaseClass

log_dir = Path(__file__).resolve().parent.parent / "ui_tests-logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / "test.log"

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
        # is_headless = True

        is_headless = os.getenv("HEADLESS", "false").lower() == "true"

        browser = playwright.chromium.launch(
            headless=is_headless,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            locale="en-US",
            viewport={"width": 1920, "height": 1080},
            screen={"width": 1920, "height": 1080}
        )

        page = context.new_page()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        base_class = BaseClass(page)
        page.goto(base_class.base_url)
        yield base_class

        try:
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
        if log_path.exists():
            with open(log_path, "r", encoding="utf-8") as log_file:
                allure.attach(
                    log_file.read(),
                    name=f"log_{item.name}",
                    attachment_type=allure.attachment_type.TEXT
                )
