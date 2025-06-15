from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class InventoryPage(BasePage):
    def add_to_cart(self, product_name):
        # First try using inventory_item_name to find the product
        try:
            # More specific and robust XPath that targets the correct button for each product
            self.click((By.XPATH, f"//div[contains(@class,'inventory_item_name') and text()='{product_name}']/ancestor::div[contains(@class,'inventory_item')]//button[contains(@class,'btn_inventory')]"))
        except:
            # Fallback method
            self.wait_for_element((By.CLASS_NAME, "inventory_item"))
            items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
            for item in items:
                item_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                if item_name == product_name:
                    item.find_element(By.CSS_SELECTOR, "button.btn_primary").click()
                    break

    def go_to_cart(self):
        self.click((By.CLASS_NAME, "shopping_cart_link"))

    def get_cart_count(self):
        return int(self.get_text((By.CLASS_NAME, "shopping_cart_badge")))
        
    def sort_by(self, option_text):
        sort_dropdown = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        sort_dropdown.select_by_visible_text(option_text)
        
    def _get_item_names(self):
        return [item.text for item in self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
        
    def _get_item_prices(self):
        return [float(price.text.replace("$", "")) for price in self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
        
    def is_sorted_by_name_ascending(self):
        names = self._get_item_names()
        return names == sorted(names)
        
    def is_sorted_by_name_descending(self):
        names = self._get_item_names()
        return names == sorted(names, reverse=True)
        
    def is_sorted_by_price_ascending(self):
        prices = self._get_item_prices()
        return prices == sorted(prices)
        
    def is_sorted_by_price_descending(self):
        prices = self._get_item_prices()
        return prices == sorted(prices, reverse=True)
