from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException

class LoginPage(BasePage):
    USERNAME_FIELD = (By.CSS_SELECTOR, "#user-name, [name='user-name'], input[placeholder*='Username']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "#password, [name='password'], input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "#login-button, [name='login-button'], button[type='submit'], .btn_action")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error'], .error-message-container, h3[data-test='error']")
    
    def login_as_standard_user(self):
        self.login("standard_user", "secret_sauce")
        
    def login(self, username, password):
        # Make sure we're on the login page
        if 'saucedemo.com' not in self.driver.current_url:
            self.driver.get("https://www.saucedemo.com/")
            
        # Wait for username field explicitly before continuing
        self.wait_for_element(self.USERNAME_FIELD)
            
        # Enter credentials
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)
        
        # Wait for page to load - either inventory page or error message
        try:
            self.wait_for_element((By.CLASS_NAME, "inventory_container"), timeout=3)
        except TimeoutException:
            # If inventory page didn't load, check if there's an error message
            try:
                # Wait explicitly for error message - important for error assertions
                self.wait_for_element(self.ERROR_MESSAGE, timeout=3)
            except TimeoutException:
                # Take a screenshot if neither inventory nor error message appears
                self.take_screenshot(f"login_failure_{username}")
        
    def get_error_message(self):
        """Get error message text with added robustness"""
        try:
            # Try multiple selectors to find the error message
            selectors = [
                self.ERROR_MESSAGE,
                (By.CSS_SELECTOR, ".error-message-container"),
                (By.CSS_SELECTOR, "h3[data-test='error']"),
                (By.CSS_SELECTOR, ".error")
            ]
            
            # Try each selector
            for selector in selectors:
                try:
                    # Take screenshot and save to screenshots folder, then attach to Allure report
                    self.take_screenshot("before_error_check")
                    return self.get_text(selector)
                except:
                    continue
                    
            # If none of the selectors worked, try a broad approach
            error_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'failed') or contains(text(), 'locked')]")
            if error_elements:
                return error_elements[0].text
            
            return ""  # Return empty string if no error message found
        except Exception as e:
            print(f"Error getting error message: {e}")
            return ""  # Return empty string if any exception occurs
