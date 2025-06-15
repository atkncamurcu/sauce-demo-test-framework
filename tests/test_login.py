import pytest
from pages.login_page import LoginPage
from utils.test_data import VALID_USERS


@pytest.mark.usefixtures("setup")
class TestLogin:

    def setup_method(self):
        # Her test öncesinde login sayfasına git
        self.driver.get("https://www.saucedemo.com/")
        # Sayfanın yüklenmesi için kısa bir bekleme
        self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        
    def teardown_method(self):
        # Her test sonrasında logout işlemi yap
        try:
            # Eğer giriş yapıldıysa, logout yap
            if "inventory" in self.driver.current_url:
                self.driver.find_element("id", "react-burger-menu-btn").click()
                self.wait.until(lambda driver: driver.find_element("id", "logout_sidebar_link").is_displayed())
                self.driver.find_element("id", "logout_sidebar_link").click()
        except:
            # Eğer zaten login sayfasındaysak, hiçbir şey yapma
            pass
        
        # Çerezleri temizle
        self.driver.delete_all_cookies()
        
        # Sayfayı yenile
        self.driver.get("https://www.saucedemo.com/")

    def test_login_with_valid_standard_user(self):
        LoginPage(self.driver).login(VALID_USERS["locked_out_user"]["username"],
                                     VALID_USERS["locked_out_user"]["password"])
        assert "inventory" in self.driver.current_url

    def test_login_with_locked_out_user(self):
        LoginPage(self.driver).login(VALID_USERS["locked_out_user"]["username"],
                                     VALID_USERS["locked_out_user"]["password"])
        assert "locked out" in LoginPage(self.driver).get_error_message().lower()

    def test_login_with_problem_user(self):
        LoginPage(self.driver).login(VALID_USERS["problem_user"]["username"],
                                     VALID_USERS["problem_user"]["password"])
        assert "inventory" in self.driver.current_url

    def test_login_with_performance_glitch_user(self):
        LoginPage(self.driver).login(VALID_USERS["performance_glitch_user"]["username"],
                                     VALID_USERS["performance_glitch_user"]["password"])
        assert "inventory" in self.driver.current_url

    def test_login_with_error_user(self):
        LoginPage(self.driver).login(VALID_USERS["error_user"]["username"],
                                     VALID_USERS["error_user"]["password"])
        assert "inventory" in self.driver.current_url

    def test_login_with_visual_user(self):
        LoginPage(self.driver).login(VALID_USERS["visual_user"]["username"],
                                     VALID_USERS["visual_user"]["password"])
        assert "inventory" in self.driver.current_url

    def test_login_with_invalid_password(self):
        LoginPage(self.driver).login("standard_user", "wrong_password")
        assert "epic sadface" in LoginPage(self.driver).get_error_message().lower()
