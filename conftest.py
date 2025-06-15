import pytest
import time
import platform
import os
import datetime
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(scope="class")
def setup(request):
    driver = None
    browser = request.config.getoption("--browser", default="firefox")
    
    if browser.lower() == "firefox":
        # First try Firefox with direct path
        try:
            print("Initializing Firefox WebDriver with local driver...")
            firefox_options = FirefoxOptions()
            
            # Use direct path to geckodriver - update this path as needed  
            driver_path = "/usr/local/bin/geckodriver"  # Common location on macOS
            service = FirefoxService(executable_path=driver_path)
            driver = webdriver.Firefox(service=service, options=firefox_options)
            print("Firefox WebDriver initialized successfully!")
        except Exception as e:
            print(f"Firefox WebDriver initialization error: {e}")
    
    # If Firefox fails or browser is Chrome, try Chrome
    if driver is None:
        try:
            print("Initializing Chrome WebDriver with local driver...")
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            
            # Use direct path to chromedriver - update this path as needed
            driver_path = "/usr/local/bin/chromedriver"  # Common location on macOS
            service = ChromeService(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Chrome WebDriver initialized successfully!")
        except Exception as e:
            print(f"Chrome WebDriver initialization error: {e}")
    
    # If both Chrome and Firefox fail, raise an exception
    if driver is None:
        raise Exception("Could not initialize any WebDriver. Please ensure chromedriver or geckodriver is installed and the path is correct.")
    
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)  # Set a reasonable implicit wait
    
    # Navigate to the site and ensure it's loaded
    driver.get("https://www.saucedemo.com/")
    
    # Wait for the login page to load with improved selectors
    wait = WebDriverWait(driver, 20)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-name, [name='user-name']")))
    except Exception as e:
        # Take screenshot on failure and attach to Allure report
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        screenshot_path = os.path.join(screenshots_dir, f"login_page_load_failure_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        
        # Attach to Allure report if available
        try:
            with open(screenshot_path, "rb") as file:
                allure.attach(
                    file.read(),
                    name=f"login_page_load_failure",
                    attachment_type=allure.attachment_type.PNG
                )
        except Exception as attach_error:
            print(f"Failed to attach screenshot to Allure report: {attach_error}")
        
        print(f"Error waiting for login page: {e}")
        print(f"Current URL: {driver.current_url}")
        print(f"Screenshot saved to: {screenshot_path}")
        
        # Try refreshing the page
        driver.refresh()
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#user-name, [name='user-name']")))
        except Exception as e:
            # Take another screenshot after refresh attempt
            screenshot_path = os.path.join(screenshots_dir, f"login_page_refresh_failure_{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            
            # Attach to Allure report
            try:
                with open(screenshot_path, "rb") as file:
                    allure.attach(
                        file.read(),
                        name=f"login_page_refresh_failure",
                        attachment_type=allure.attachment_type.PNG
                    )
            except Exception as attach_error:
                print(f"Failed to attach screenshot to Allure report: {attach_error}")
                
            driver.quit()
            raise Exception(f"Login page failed to load properly: {e}")
        
    request.cls.driver = driver
    request.cls.wait = wait  # Add a wait object to the test class for explicit waits
    
    # Add driver and wait to the class
    request.cls.driver = driver
    request.cls.wait = wait
    
    # Return control to the test
    yield
    
    # Cleanup after all tests in the class
    try:
        # Clear cookies and storage to reset state between tests
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
    except:
        pass
    
    # Quit the driver
    if driver:
        driver.quit()
        
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox", 
                     help="Browser to run tests: 'chrome' or 'firefox' (default: firefox)")
                     
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failures and attach them to Allure report
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            driver = item.instance.driver
            
            # Create screenshots directory if it doesn't exist
            screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)
                
            # Generate unique screenshot filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.nodeid.replace("/", "_").replace("::", "_").replace(".py", "")
            screenshot_name = f"failure_{test_name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshots_dir, screenshot_name)
            
            # Take screenshot
            driver.save_screenshot(screenshot_path)
            
            # Attach to Allure report
            try:
                with open(screenshot_path, "rb") as file:
                    allure.attach(
                        file.read(),
                        name=f"Failure in {test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                print(f"Screenshot saved to: {screenshot_path} and attached to Allure report")
            except Exception as e:
                print(f"Failed to attach screenshot to Allure report: {e}")
                
        except Exception as e:
            print(f"Failed to capture screenshot on test failure: {e}")
