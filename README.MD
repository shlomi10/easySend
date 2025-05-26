# 🚀 EasySend - Todo App Test Automation

<div align="center">

[![Python](https://img.shields.io/badge/python-v3.12+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-latest-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/pytest-latest-orange.svg)](https://pytest.org/)
[![Allure](https://img.shields.io/badge/allure-reports-yellow.svg)](https://docs.qameta.io/allure/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/shlomi10/EasySend/workflow.yml?label=CI%20Build&style=for-the-badge&logo=github-actions)](https://github.com/shlomi10/EasySend/actions)
[![Allure Report](https://img.shields.io/badge/Allure%20Report-View%20Live-purple?style=for-the-badge&logo=github)](https://shlomi10.github.io/EasySend/)


**Modern E2E Test Automation Framework for Todo Web Application**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Overview

This project provides comprehensive end-to-end test automation for a React-based Todo application using modern testing technologies. Built with **Playwright**, **pytest**, and **Allure reporting**, it offers robust, scalable, and maintainable test automation.

### 🎯 Application Under Test
- **URL**: https://react-cool-todo-app.netlify.app/
- **Type**: React-based Todo Management Application
- **Features**: Task creation, editing, deletion, completion tracking, and filtering

## ✨ Features

### 🔧 **Core Capabilities**
- ✅ **Cross-browser testing** with Playwright
- ✅ **Page Object Model** architecture
- ✅ **Parallel test execution** for faster results
- ✅ **Allure reporting** with screenshots and traces
- ✅ **Docker containerization** for consistent environments
- ✅ **CI/CD integration** with GitHub Actions
- ✅ **Comprehensive logging** and debugging support

### 🧪 **Test Coverage**

#### **Task Creation Tests**
- **Basic Task Addition**: Create tasks with valid input (parameterized testing)
- **Empty Input Validation**: Verify behavior when submitting empty task forms
- **Character Limit Enforcement**: Ensure tasks exceeding 40 characters are blocked
- **Multiple Task Creation**: Add multiple tasks sequentially and verify order/count
- **Input Field Validation**: Comprehensive form validation testing

#### **Task Management Tests**
- **Task Completion**: Mark tasks as complete and verify status change
- **Task Editing**: Edit existing tasks and validate name changes
- **Task Deletion**: Remove tasks and verify removal from list
- **Task Status Tracking**: Monitor task completion states
- **Order Preservation**: Ensure tasks maintain proper display order

#### **Task Filtering & Display**
- **Completed Task Filtering**: Filter and display only completed tasks
- **Task Count Validation**: Verify completed task counts match between title and board
- **Visual State Verification**: Check UI indicators for task states
- **Dynamic Content Updates**: Validate real-time UI updates

#### **Error Handling & Validation**
- **Empty Input Validation**: Prevent submission of empty tasks
- **Character Limit Enforcement**: Validate 40-character task name limit
- **Error Message Display**: Verify appropriate error messages are shown
- **Form State Management**: Test form validation states

#### **User Workflow Testing**
- **Complete Task Lifecycle**: End-to-end task creation to completion
- **Navigation Flow**: Test navigation between different screens
- **Multi-task Operations**: Handle multiple tasks simultaneously
- **State Persistence**: Verify task states persist across interactions

#### **Performance Testing**
- **High Volume Task Handling**: Test application with 100+ tasks to validate scalability
- **UI Responsiveness**: Measure UI response times under load conditions
- **Page Load Performance**: Measure and validate page load time under a threshold
- **Mass Task Handling**: Add 100 tasks and verify app responsiveness

### 📊 **Reporting & Monitoring**
- Beautiful Allure HTML reports
- Automatic screenshot capture on failures
- Detailed execution traces
- Structured logging with timestamps

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (optional)
- Git

### 1. Clone Repository
```bash
git clone https://github.com/shlomi10/EasySend.git
cd EasySend
```

### 2. Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pytest-xdist  # For parallel execution

# Install Playwright browsers
playwright install --with-deps
```

### 3. Configure Environment
```bash
# Copy and edit environment variables
cp utils/.env.example utils/.env
```

Edit `utils/.env`:
```env
BASE_URL=https://react-cool-todo-app.netlify.app/
```

### 4. Run Tests

#### 🖥️ **Local Execution**
```bash
# Run all tests
pytest tests/

# Run with parallel execution (faster)
pytest tests/ -n auto

# Run with specific number of workers
pytest tests/ -n 4

# Run with Allure reporting
pytest tests/ --alluredir=allure-results

# Run parallel with Allure reporting
pytest tests/ -n auto --alluredir=allure-results

# Generate and open Allure report
allure serve allure-results
```

#### 🐳 **Docker Execution**
```bash
# Run tests in Docker with Allure server
docker-compose up --build

# Access Allure reports at http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html

# Run with parallel execution in Docker
docker-compose run tests pytest tests/ -n auto --alluredir=./allure-results
```

#### 🎭 **Headed Mode (for debugging)**
```bash
# Set environment variable
export HEADLESS=false  # Linux/macOS
set HEADLESS=false     # Windows

# Run tests
pytest tests/
```

## 📁 Project Structure

```
EasySend/
├── 📂 pages/                    # Page Object Model
│   ├── add_task_page.py        # Add task functionality
│   ├── base_page.py            # Base page methods
│   ├── edit_task_page.py       # Edit task functionality
│   └── todo_page.py            # Main todo page
├── 📂 tests/                   # Test suites
│   ├── base_class.py           # Test base class
│   ├── conftest.py             # Pytest fixtures
│   └── test_tasks.py           # Main test cases
├── 📂 utils/                   # Utilities
│   └── .env                    # Environment variables
├── 📂 .github/workflows/       # CI/CD
│   └── workflow.yml            # GitHub Actions
├── 🐳 docker-compose.yml       # Docker orchestration
├── 🐳 Dockerfile               # Docker image
├── 📋 requirements.txt         # Python dependencies
└── 📖 README.md               # This file
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `BASE_URL` | Application URL | `https://react-cool-todo-app.netlify.app/` |

### Test Execution Options
```bash
# Run specific test
pytest tests/test_tasks.py::TestToDoWebApp::test_add_task

# Run with parallel execution (recommended)
pytest tests/ -n auto

# Run with specific number of parallel workers
pytest tests/ -n 4

# Run with specific browser
pytest tests/ --browser=firefox

# Run with multiple browsers in parallel
pytest tests/ --browser=chromium --browser=firefox -n auto

# Run with verbose output
pytest tests/ -v -s

# Run parallel with custom markers
pytest tests/ -m "not slow" -n auto
```

## 📊 Reporting

### Allure Reports
The framework generates comprehensive Allure reports with:
- ✅ Test execution summary
- 📸 Screenshots on failures
- 🔍 Detailed step-by-step execution
- 📋 Test categorization and filtering
- 📈 Historical trends

### Access Reports
- **Local**: `allure serve allure-results`
- **Docker**: `http://localhost:5050/allure-docker-service/projects/default/reports/latest/index.html`
- **CI/CD**: Download artifacts from GitHub Actions
- **Live Report**: [View Live Allure Report](https://shlomi10.github.io/EasySend/)

## 🛠️ Development

### Adding New Tests
1. Create test methods in `tests/test_tasks.py`
2. Use appropriate Allure decorations
3. Follow the existing pattern for page interactions

### Adding New Pages
1. Create new page class in `pages/`
2. Inherit from `BasePage`
3. Define locators and methods
4. Add to `BaseClass` initialization

### Example Test
```python
@allure.feature("Task Management")
@allure.story("New feature test")
def test_new_feature(self, initialize):
    todo = initialize.todo_page
    # Test implementation
    assert condition
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
- ✅ Automated testing on push/PR
- ✅ Multi-environment support
- ✅ Allure report generation
- ✅ Artifact storage

### Pipeline Triggers
- Push to `main` branch
- Pull requests
- Manual workflow dispatch

## 🐳 Docker Support

### Benefits
- Consistent testing environment
- Easy CI/CD integration
- Isolated dependencies
- **Parallel execution support**
- Scalable test execution

### Commands
```bash
# Build and run
docker-compose up --build

# Run specific service
docker-compose run tests

# Run with parallel execution
docker-compose run tests pytest tests/ -n auto --alluredir=./allure-results

# View logs
docker-compose logs tests
```

## 🤝 Contributing

### Guidelines
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add appropriate Allure decorations
- Include comprehensive logging
- Write descriptive commit messages

## 📞 Support

### Getting Help
- 🐛 **Issues**: [GitHub Issues](https://github.com/shlomi10/EasySend/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/shlomi10/EasySend/discussions)
- 📧 **Contact**: Create an issue for support requests

### Common Issues
- **Browser installation**: Run `playwright install --with-deps`
- **Permission errors**: Check file permissions in Docker
- **Port conflicts**: Modify ports in `docker-compose.yml`
- **Parallel execution issues**: Reduce worker count with `-n 2` instead of `-n auto`
- **Memory issues**: Use fewer parallel workers or increase system resources

## 📈 Roadmap

- [ ] **API Testing Integration**
- [ ] **Performance Testing**
- [ ] **Visual Regression Testing**
- [ ] **Mobile Testing Support**
- [ ] **Test Data Management**
- [ ] **Enhanced Reporting Dashboard**

## 🧠 Additional Notes

- The framework dynamically validates UI form constraints like max character limits and mandatory fields.
- Stress testing simulates real-world user bulk-input scenarios with >100 tasks.


## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by [shlomi10](https://github.com/shlomi10)**

⭐ **Star this repo if you find it helpful!** ⭐

</div>