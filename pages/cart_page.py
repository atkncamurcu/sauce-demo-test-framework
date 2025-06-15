from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    def is_item_in_cart(self, item_name):
        # Wait for at least one cart item to be present or return False if none are found
        try:
            self.wait_for_element((By.CLASS_NAME, "cart_item"), timeout=5)
            items = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
            return any(item.text == item_name for item in items)
        except:
            return False

    def remove_item(self, item_name):
        try:
            # More specific XPath targeting the remove button for the specific item
            self.click((By.XPATH, f"//div[contains(@class,'inventory_item_name') and text()='{item_name}']/ancestor::div[contains(@class,'cart_item')]//button[contains(@class,'cart_button')]"))
        except:
            # Fallback - find all cart items and click the remove button for matching item
            items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
            for item in items:
                if item_name in item.text:
                    item.find_element(By.CSS_SELECTOR, "button").click()
                    break

    def is_cart_empty(self):
        # First check if there's a "Your cart is empty" message
        try:
            empty_msg = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'empty') or contains(text(), 'Empty')]")
            if empty_msg:
                return True
        except:
            pass
            
        # Then check if there are cart items
        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        return len(cart_items) == 0

    def get_cart_items_count(self):
        try:
            # Wait for cart items to load
            self.wait_for_element((By.CLASS_NAME, "cart_item"), timeout=5)
            return len(self.driver.find_elements(By.CLASS_NAME, "cart_item"))
        except:
            return 0

    def click_checkout(self):
        self.click((By.ID, "checkout"))
