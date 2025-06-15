import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.mark.usefixtures("setup")
class TestCheckout:
    def setup_method(self):
        # Navigate to homepage at the start of each test
        self.driver.get("https://www.saucedemo.com/")
        
    def teardown_method(self):
        # Log out properly after each test
        try:
            # If we're on an inventory, cart, or checkout page, logout
            if any(x in self.driver.current_url for x in ["inventory", "cart", "checkout"]):
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
        
    def test_successful_checkout(self):
        LoginPage(self.driver).login_as_standard_user()
        inventory = InventoryPage(self.driver)
        inventory.add_to_cart("Sauce Labs Backpack")
        inventory.go_to_cart()
        cart = CartPage(self.driver)
        cart.click_checkout()
        checkout = CheckoutPage(self.driver)
        checkout.fill_information("John", "Doe", "12345")
        checkout.finish_checkout()
        assert checkout.is_checkout_complete()
