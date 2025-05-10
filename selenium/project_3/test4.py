from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(3)

    def test_short_password_and_invalid_email(self):
        driver = self.driver

        # ----------- Part 1: Login Page ------------

        # Short password
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        email_input.clear()
        email_input.send_keys("test@example.com")
        time.sleep(1)
        password_input.clear()
        password_input.send_keys("123")
        time.sleep(1)
        login_button.click()
        time.sleep(2)


        # Try again with valid credentials
        password_input.clear()
        password_input.send_keys("abc123")
        time.sleep(1)
        login_button.click()
        time.sleep(5)

        # ----------- Part 2: Survey Page ------------

        driver.find_element(By.ID, "name_surname").send_keys("Remus Lupin")
        time.sleep(1)
        driver.find_element(By.ID, "birth_day").send_keys("15")
        driver.find_element(By.ID, "birth_month").send_keys("3")
        driver.find_element(By.ID, "birth_year").send_keys("1985")
        time.sleep(1)
        driver.find_element(By.ID, "education_level").send_keys("PhD")
        driver.find_element(By.ID, "city").send_keys("Hogwarts")
        time.sleep(1)
        driver.find_element(By.ID, "gender-male").click()
        time.sleep(1)
        driver.find_element(By.ID, "model-ChatGPT").click()
        time.sleep(1)
        driver.find_element(By.ID, "defect-ChatGPT").send_keys("Too cheerful.")
        time.sleep(1)
        driver.find_element(By.ID, "beneficial_use").send_keys("Teaching defense.")
        time.sleep(1)

        # Invalid email format (missing domain)
        survey_email = driver.find_element(By.ID, "email")
        survey_email.clear()
        survey_email.send_keys("lupin@")
        time.sleep(2)

        submit_button = driver.find_element(By.ID, "submit-button")
        self.assertFalse(submit_button.is_enabled())
        time.sleep(2)

        # Invalid email (missing @)
        survey_email.clear()
        survey_email.send_keys("lupinhogwarts.com")
        time.sleep(2)
        self.assertFalse(submit_button.is_enabled())
        time.sleep(2)

        # Valid email
        survey_email.clear()
        survey_email.send_keys("lupin@hogwarts.com")
        time.sleep(3)
        self.assertTrue(submit_button.is_enabled())

        submit_button.click()
        time.sleep(5)

        self.assertIn("Thank you", driver.page_source)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
