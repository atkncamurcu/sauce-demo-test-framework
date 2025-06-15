from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import allure
import datetime

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    def take_screenshot(self, name):
        """Take a screenshot and attach it to the Allure report"""
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            
        # Generate a timestamp for unique filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(screenshots_dir, f"{name}_{timestamp}.png")
        
        # Take screenshot and save to file
        self.driver.save_screenshot(screenshot_path)
        
        # Attach to Allure report if available
        try:
            with open(screenshot_path, "rb") as file:
                allure.attach(
                    file.read(),
                    name=f"{name}",
                    attachment_type=allure.attachment_type.PNG
                )
            return screenshot_path
        except Exception as e:
            print(f"Failed to attach screenshot to Allure report: {e}")
            return screenshot_path
    
    def wait_for_element(self, by_locator, timeout=10):
        """Wait for element to be present in the DOM"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(by_locator)
            )
        except TimeoutException:
            # Take screenshot on failure and attach to Allure report
            self.take_screenshot(f"element_not_found_{by_locator[1]}")
            raise

    def click(self, by_locator):
        """Click an element after waiting for it to be clickable"""
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(by_locator)
        )
        element.click()

    def enter_text(self, by_locator, text):
        """Enter text in an element after waiting for it to be visible"""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        )
        element.clear()
        element.send_keys(text)

    def get_text(self, by_locator):
        """Get text from an element after waiting for it to be visible"""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(by_locator)
        )
        return element.text
        
    def is_visible(self, by_locator):
        """Check if element is visible"""
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(by_locator)
            ).is_displayed()
        except TimeoutException:
            return False
