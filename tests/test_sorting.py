import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.test_data import standard_user


@pytest.mark.usefixtures("setup")
@pytest.mark.sorting
class TestSorting:
    def setup_method(self):
        # Navigate to homepage at the start of each test
        self.driver.get("https://www.saucedemo.com/")
        
    def teardown_method(self):
        # Log out properly after each test
        try:
            # If we're on inventory page, logout
            if "inventory" in self.driver.current_url:
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

    def test_sort_items_by_name_az(self):
        LoginPage(self.driver).login_as_standard_user()
        inventory = InventoryPage(self.driver)
        inventory.sort_by("Name (A to Z)")
        assert inventory.is_sorted_by_name_ascending()

    def test_sort_items_by_name_za(self):
        LoginPage(self.driver).login_as_standard_user()
        inventory = InventoryPage(self.driver)
        inventory.sort_by("Name (Z to A)")
        assert inventory.is_sorted_by_name_descending()

    def test_sort_items_by_price_lohi(self):
        LoginPage(self.driver).login_as_standard_user()
        inventory = InventoryPage(self.driver)
        inventory.sort_by("Price (low to high)")
        assert inventory.is_sorted_by_price_ascending()

    def test_sort_items_by_price_hilo(self):
        LoginPage(self.driver).login_as_standard_user()
        inventory = InventoryPage(self.driver)
        inventory.sort_by("Price (high to low)")
        assert inventory.is_sorted_by_price_descending()
