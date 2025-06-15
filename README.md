# Sauce Demo Test Automation Framework

This is an automated testing framework for the [Sauce Demo](https://www.saucedemo.com/) website using Python, Selenium, and Pytest.

## Overview

This framework uses a Page Object Model (POM) design pattern to create an abstraction layer for the web UI elements. This makes the test scripts more maintainable and reusable.

## Project Structure

```
sauce-demo-test-framework/
├── conftest.py             # Pytest fixtures and configurations
├── pytest.ini              # Pytest settings
├── pages/                  # Page objects
│   ├── base_page.py        # Base class for all page objects
│   ├── login_page.py       # Login page elements and actions
│   ├── inventory_page.py   # Inventory page elements and actions
│   ├── cart_page.py        # Cart page elements and actions
│   └── checkout_page.py    # Checkout page elements and actions
├── tests/                  # Test cases
│   ├── test_login.py       # Login functionality tests
│   ├── test_cart.py        # Shopping cart tests
│   ├── test_checkout.py    # Checkout process tests
│   └── test_sorting.py     # Product sorting tests
├── utils/                  # Utility modules
│   └── test_data.py        # Test data like user credentials
└── requirements.txt        # Project dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- Chrome or Firefox browser
- pip (Python package manager)

### Installation

1. Clone this repository or download the source code

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### WebDriver Setup

To avoid GitHub API rate limit issues, this framework is configured to use locally installed WebDrivers. Follow these steps to set up your environment:

#### Chrome WebDriver Setup

1. Determine which version of Chrome you have installed:
   - Open Chrome
   - Click the three dots in the top-right corner
   - Navigate to Help > About Google Chrome
   - Note the version number (e.g., 137.0.7151.70)

2. Download the matching ChromeDriver:
   - Go to https://chromedriver.chromium.org/downloads
   - Download the version that matches your Chrome version
   - For macOS on M1/M2/M3 (Apple Silicon), download the arm64 version if available

3. Install the ChromeDriver:
   - Unzip the downloaded file
   - Move the chromedriver executable to `/usr/local/bin/` (requires sudo):
     ```bash
     sudo mv chromedriver /usr/local/bin/
     sudo chmod +x /usr/local/bin/chromedriver
     ```

#### Firefox WebDriver (GeckoDriver) Setup

1. Download the latest GeckoDriver:
   - Go to https://github.com/mozilla/geckodriver/releases
   - Download the appropriate version for macOS

2. Install the GeckoDriver:
   - Unzip the downloaded file
   - Move the geckodriver executable to `/usr/local/bin/` (requires sudo):
     ```bash
     sudo mv geckodriver /usr/local/bin/
     sudo chmod +x /usr/local/bin/geckodriver
     ```

#### Verify Installation

After installation, you should be able to run these commands to verify that the drivers are properly installed:

```bash
chromedriver --version
geckodriver --version
```

#### Updating the Framework Configuration

If you installed the drivers in a location other than `/usr/local/bin/`, update the paths in the `conftest.py` file:

```python
# For Chrome

## Continuous Integration

This project is configured to run tests automatically using GitHub Actions. Tests will run on:

- Every push to the main branch
- Every pull request to the main branch

### GitHub Actions Workflow

The CI workflow:
1. Sets up a Python environment
2. Installs project dependencies
3. Sets up Chrome and ChromeDriver
4. Runs the tests
5. Uploads test artifacts (reports and screenshots)

### CI Configuration

The GitHub Actions workflow is defined in `.github/workflows/test.yml`. 

If you need to modify the CI configuration, you can edit this file. The workflow is set to:

- Run on Ubuntu latest
- Use Python 3.11
- Use actions/checkout@v4
- Use actions/setup-python@v5
- Use actions/upload-artifact@v4
- Run in headless mode

### Viewing Test Results

After a CI run completes, you can view:
- The test execution logs in the GitHub Actions tab
- Test artifacts (screenshots and reports) by downloading the uploaded artifacts from the workflow run page
driver_path = "/path/to/your/chromedriver"  # Update this path
service = ChromeService(executable_path=driver_path)

# For Firefox
driver_path = "/path/to/your/geckodriver"  # Update this path
service = FirefoxService(executable_path=driver_path)
```

## Running the Tests

### Run all tests:

```bash
pytest
```

### Run specific test file:

```bash
pytest tests/test_login.py
```

### Run tests with verbose output:

```bash
pytest -v
```

### Run tests and generate HTML report:

```bash
pytest --html=report.html
```

### Run tests with Allure reporting:

```bash
pytest --alluredir=./reports
```

### Run tests with specific browser:

```bash
# Run with Firefox (default)
pytest --browser=firefox

# Run with Chrome
pytest --browser=chrome

# Run with Firefox and generate Allure reports
pytest --browser=firefox --alluredir=./reports
```

## Test Reports

### HTML Reports
After running the tests with the HTML report option, you can open the generated `report.html` file in a browser to view the test results.

### Allure Reports
Allure provides more detailed and interactive reports. To generate and view Allure reports:

1. Install Allure command-line tool:
   
   On macOS:
   ```bash
   brew install allure
   ```
   
   On Linux:
   ```bash
   sudo apt-add-repository ppa:qameta/allure
   sudo apt-get update
   sudo apt-get install allure
   ```
   
   On Windows with Scoop:
   ```bash
   scoop install allure
   ```

2. Run tests with Allure results generation:
   ```bash
   pytest --alluredir=./reports
   ```

3. Generate and open the Allure report:
   ```bash
   allure serve ./reports
   ```

4. For generating a static report:
   ```bash
   allure generate ./reports -o ./allure-report --clean
   ```
   Then open `./allure-report/index.html` in your browser.

## Framework Features

- Page Object Model design pattern
- Explicit waits for better stability
- Screenshot capture on test failures
- Proper cleanup between tests
- Improved error handling
- HTML reports generation
- Allure reporting integration for detailed test reports
- Parallel test execution capability with pytest-xdist
- Cross-browser testing support (Chrome and Firefox)
