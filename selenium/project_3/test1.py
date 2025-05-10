from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class FullFlowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")  # Your frontend URL
        time.sleep(3)  # Let the page load

    def test_login_and_survey_submission(self):
        driver = self.driver

        # ----------- Part 1: Login Page ------------

        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.ID, "login-button")

        # 1. Try login with empty password
        email_input.clear()
        email_input.send_keys("test@example.com")
        time.sleep(1)
        password_input.clear()
        time.sleep(1)
        login_button.click()
        time.sleep(3)

        # 2. Try login with valid credentials
        password_input.send_keys("abc123")
        time.sleep(1)
        login_button.click()
        time.sleep(5)  # Wait for redirect

        self.assertIn("AI Usage Survey", driver.page_source)  # Adjust to real text

        # ----------- Part 2: Survey Page ------------

        driver.find_element(By.ID, "name_surname").send_keys("John Doe")
        time.sleep(1)
        driver.find_element(By.ID, "birth_day").send_keys("10")
        time.sleep(1)
        driver.find_element(By.ID, "birth_month").send_keys("5")
        time.sleep(1)
        driver.find_element(By.ID, "birth_year").send_keys("1999")
        time.sleep(1)
        driver.find_element(By.ID, "education_level").send_keys("Undergraduate")
        time.sleep(1)

        # Leave city empty
        driver.find_element(By.ID, "gender-male").click()
        time.sleep(1)
        driver.find_element(By.ID, "model-ChatGPT").click()
        time.sleep(1)
        driver.find_element(By.ID, "defect-ChatGPT").send_keys("Sometimes gives hallucinated answers")
        time.sleep(1)
        driver.find_element(By.ID, "beneficial_use").send_keys("Helps with coding.")
        time.sleep(1)
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        time.sleep(1)

        submit_button = driver.find_element(By.ID, "submit-button")
        self.assertFalse(submit_button.is_enabled())
        time.sleep(2)

        # Now fill the city
        driver.find_element(By.ID, "city").send_keys("Ankara")
        time.sleep(2)

        self.assertTrue(submit_button.is_enabled())
        submit_button.click()
        time.sleep(5)

        self.assertIn("Thank you", driver.page_source)  # Adjust as needed

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
