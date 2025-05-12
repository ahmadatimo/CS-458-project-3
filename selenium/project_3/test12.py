from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCase12(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(2)

    def test_lockout_and_multilingual_labels(self):
        driver = self.driver

        # ----------- PART 1: Trigger Lockout by entering wrong password 5 times -----------
        for _ in range(5):
            email = driver.find_element(By.ID, "email")
            password = driver.find_element(By.ID, "password")
            email.clear()
            email.send_keys("david.green@example.com")
            password.clear()
            password.send_keys("wrong234")
            driver.find_element(By.ID, "login-button").click()
            time.sleep(1)

        # Wait 60 seconds to unlock
        time.sleep(60)

        # ----------- Retry with correct credentials -----------
        email = driver.find_element(By.ID, "email")
        password = driver.find_element(By.ID, "password")
        email.clear()
        email.send_keys("david.green@example.com")
        password.clear()
        password.send_keys("david2025")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(5)

        # ----------- PART 2: Create a Question and Go to Fill Survey -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.send_keys("Your favorite programming language?")
        time.sleep(1)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(2)

        # ----------- PART 3: Fill the Question BEFORE fixing the email -----------
        text_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        text_input.send_keys("Python")
        time.sleep(2)

        # ----------- PART 4: Email '.com' Validation -----------
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        time.sleep(1)

        email_input.clear()
        email_input.send_keys("user@domain")  # Missing .com
        time.sleep(2)
        self.assertFalse(submit_button.is_enabled(), "❌ Submit button should be disabled for invalid email")

        email_input.clear()
        email_input.send_keys("user@domain.com")
        time.sleep(2)
        self.assertTrue(submit_button.is_enabled(), "✅ Submit button should be enabled after valid email + answer")

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
