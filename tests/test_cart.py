import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

@pytest.mark.usefixtures("setup")
class TestCart:
    def setup_method(self):
        # Navigate to homepage at the start of each test
        self.driver.get("https://www.saucedemo.com/")
        
    def teardown_method(self):
        # Log out properly after each test
        try:
            # If we're on an inventory or cart page, logout
            if any(x in self.driver.current_url for x in ["inventory", "cart"]):
                self.driver.find_element("id", "react-burger-menu-btn").click()
                self.wait.until(lambda driver: driver.find_element("id", "logout_sidebar_link").is_displayed())
                self.driver.find_element("id", "logout_sidebar_link").click()
        except Exception as e:
            print(f"Logout failed: {e}")
            
        # Clear cookies and local storage
        self.driver.delete_all_cookies()
        try:
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.execute_script("window.sessionStorage.clear();")
        except:
            pass
            
        # Return to login page
        self.driver.get("https://www.saucedemo.com/")

    def test_add_single_product_to_cart(self):
        LoginPage(self.driver).login_as_standard_user()
        inventory = InventoryPage(self.driver)
        inventory.add_to_cart("Sauce Labs Backpack")
        inventory.go_to_cart()
        assert CartPage(self.driver).is_item_in_cart("Sauce Labs Backpack")

    def test_remove_product_from_cart(self):
        LoginPage(self.driver).login_as_standard_user()
        inventory = InventoryPage(self.driver)
        inventory.add_to_cart("Sauce Labs Backpack")
        inventory.go_to_cart()
        cart = CartPage(self.driver)
        cart.remove_item("Sauce Labs Backpack")
        assert not cart.is_item_in_cart("Sauce Labs Backpack")

    def test_empty_cart_has_no_items(self):
        LoginPage(self.driver).login_as_standard_user()
        InventoryPage(self.driver).go_to_cart()
        assert CartPage(self.driver).is_cart_empty()

    def test_cart_shows_correct_item_count(self):
        LoginPage(self.driver).login_as_standard_user()
        inventory = InventoryPage(self.driver)
        inventory.add_to_cart("Sauce Labs Backpack")
        inventory.add_to_cart("Sauce Labs Bike Light")
        assert inventory.get_cart_count() == 2
        inventory.go_to_cart()
        assert CartPage(self.driver).get_cart_items_count() == 2
