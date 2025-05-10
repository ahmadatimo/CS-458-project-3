from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(3)

    def test_long_password_and_max_chars(self):
        driver = self.driver

        # ----------- Part 1: Login Page ------------

        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        email_input.clear()
        email_input.send_keys("test@example.com")
        time.sleep(1)

        # Long password (>15 chars)
        long_password = "abcdefghijklmnopqrstu"
        password_input.clear()
        password_input.send_keys(long_password)
        time.sleep(1)
        login_button.click()
        time.sleep(2)

        # Valid login
        password_input.clear()
        password_input.send_keys("abc123")
        time.sleep(1)
        login_button.click()
        time.sleep(4)

        # ----------- Part 2: Survey Page ------------

        driver.find_element(By.ID, "name_surname").send_keys("Sirius Black")
        time.sleep(1)
        driver.find_element(By.ID, "birth_day").send_keys("12")
        driver.find_element(By.ID, "birth_month").send_keys("11")
        driver.find_element(By.ID, "birth_year").send_keys("1980")
        time.sleep(1)
        driver.find_element(By.ID, "education_level").send_keys("Postgraduate")
        driver.find_element(By.ID, "city").send_keys("London")
        driver.find_element(By.ID, "gender-male").click()
        time.sleep(1)
        driver.find_element(By.ID, "model-Gemini").click()
        driver.find_element(By.ID, "defect-Gemini").send_keys("Sometimes too vague.")
        time.sleep(1)
        driver.find_element(By.ID, "email").send_keys("sirius@order.org")
        time.sleep(1)

        # Enter >150 characters into "Beneficial Use"
        long_text = "Hey,This is a long sentence that goes beyond 150 characters just to test if the beneficial use field can stop further input. Let's see if it gets cut.............................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................."


        beneficial_input = driver.find_element(By.ID, "beneficial_use")
        beneficial_input.send_keys(long_text)
        time.sleep(2)

        # Get value and character count
        current_value = beneficial_input.get_attribute("value")
        char_count = len(current_value)

        print(f"Typed characters: {char_count}")
        self.assertLessEqual(char_count, 150)

        # Confirm counter is updating
        self.assertIn(f"{150 - char_count} characters left", driver.page_source)

        submit_button = driver.find_element(By.ID, "submit-button")
        self.assertTrue(submit_button.is_enabled())
        time.sleep(1)

        submit_button.click()
        time.sleep(4)

        self.assertIn("Thank you", driver.page_source)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
