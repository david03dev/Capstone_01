from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import unittest

# Locators and Configurations for OrangeHRM
class OrangeHRM_Locators:
    username = "username"
    password = "password"
    submit_button = "//button[@type='submit']"
    url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    dashboard_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    excel_file = "D:\\Guvi - Automation testing\\Capstone projects\\test_data.xlsx"
    #D:\Guvi - Automation testing\Capstone projects
    sheet_number = "Sheet1"
    pass_data = "TEST PASS"
    fail_data = "TEST FAILED"

# Page Object for Login Page
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.NAME, OrangeHRM_Locators.username)
        self.password_input = (By.NAME, OrangeHRM_Locators.password)
        self.login_button = (By.XPATH, OrangeHRM_Locators.submit_button)

    def enter_username(self, username):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.username_input)
        ).send_keys(username)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_input)
        ).send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_button)
        ).click()

# Page Object for PIM Page
class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.pim_menu = (By.ID, "menu_pim_viewPimModule")
        self.add_employee_button = (By.ID, "btnAdd")
        self.first_name_input = (By.ID, "firstName")
        self.last_name_input = (By.ID, "lastName")
        self.save_button = (By.ID, "btnSave")

    def go_to_pim(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.pim_menu)
        ).click()

    def add_employee(self, first_name, last_name):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.add_employee_button)
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.first_name_input)
        ).send_keys(first_name)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.last_name_input)
        ).send_keys(last_name)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.save_button)
        ).click()

# Test cases for OrangeHRM
class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(OrangeHRM_Locators.url)

    def test_valid_login(self):
        login = LoginPage(self.driver)
        login.enter_username("Admin")
        login.enter_password("admin123")
        login.click_login()
        
        # Assert that the user has successfully navigated to the dashboard page
        WebDriverWait(self.driver, 10).until(
            EC.url_contains(OrangeHRM_Locators.dashboard_url)
        )
        self.assertIn("dashboard", self.driver.current_url)

    def test_invalid_login(self):
        login = LoginPage(self.driver)
        login.enter_username("Admin")
        login.enter_password("InvalidPassword")
        login.click_login()
        
        error_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Invalid credentials')]"))
        ).text
        self.assertEqual(error_message, "Invalid credentials")

    def tearDown(self):
        self.driver.quit()

# Test cases for PIM module
class TestPIM(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(OrangeHRM_Locators.url)
        
        # Log in first
        login = LoginPage(self.driver)
        login.enter_username("Admin")
        login.enter_password("admin123")
        login.click_login()

    def test_add_employee(self):
        pim = PIMPage(self.driver)
        pim.go_to_pim()
        pim.add_employee("David", "Selvaraj")
        # Add assertion to check if the employee was added successfully
        success_message = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='message success fadable']"))
        ).text
        self.assertIn("Successfully Saved", success_message)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
