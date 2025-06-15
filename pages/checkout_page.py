from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    def fill_information(self, first_name, last_name, postal_code):
        self.enter_text((By.ID, "first-name"), first_name)
        self.enter_text((By.ID, "last-name"), last_name)
        self.enter_text((By.ID, "postal-code"), postal_code)
        self.click((By.ID, "continue"))

    def finish_checkout(self):
        self.click((By.ID, "finish"))

    def is_checkout_complete(self):
        return "Thank you for your order!" in self.get_text((By.CLASS_NAME, "complete-header"))
