from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import unittest

class TestCase9(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(3)

    def test_email_and_invalid_questions(self):
        driver = self.driver

        # ---- Login: Invalid Email (user@)
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")

        email_input.send_keys("user@")
        password_input.send_keys("abc123")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # HTML5 validation error
        self.assertNotEqual(email_input.get_attribute("validationMessage"), "")

        # ---- Login: Valid credentials
        email_input.clear()
        email_input.send_keys("test@example.com")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(4)

        # ---- Navigate to Survey Builder
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(3)

        # ---- Attempt to add question with only spaces
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.send_keys("   ")
        time.sleep(1)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(1)

        # Should not be added — preview remains empty
        self.assertIn("No questions yet", driver.page_source)

        # ---- Try adding multiple choice with empty options
        label_input.clear()
        label_input.send_keys("Favorite color?")
        time.sleep(1)

        # Select multiple choice
        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        type_dropdown.find_element(By.XPATH, ".//option[@value='multiple_choice']").click()
        time.sleep(1)

        # Clear default option 0
        option_0 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']")
        option_0.clear()
        time.sleep(0.5)

        # Add a duplicate empty option
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        time.sleep(0.5)
        option_1 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']")
        option_1.clear()
        option_1.send_keys("")
        time.sleep(0.5)

        # Try to submit
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(1)

        # Should still not add
        self.assertIn("No questions yet", driver.page_source)

        # ---- Try with duplicate labels
        option_0.send_keys("Red")
        option_1.send_keys("Red")
        time.sleep(1)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(1)
        
        option_0.clear()
        
        option_0.send_keys("Blue")
        time.sleep(1)
        time.sleep(0.5)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(1)

        # Should also fail due to non-unique options
        self.assertIn("No questions yet", driver.page_source)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
