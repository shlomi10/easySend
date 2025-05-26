FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

# Install xvfb and dependencies
RUN apt-get update && apt-get install -y xvfb

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps

COPY . .

RUN mkdir -p ./allure-results ./screenshots ./trace ./todo-tests-logs

ENV PYTHONPATH=/app
ENV HEADLESS=false

# If you want to run with Xvfb for headed mode testing
# CMD ["xvfb-run", "-a", "pytest", "tests/", "--alluredir=./allure-results"]

# Default to headless mode which is more reliable in Docker
CMD ["xvfb-run", "-a", "pytest", "tests/", "--alluredir=./allure-results"]