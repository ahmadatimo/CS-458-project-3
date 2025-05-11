from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import unittest

class TestCase8(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(2)

    def test_email_format_and_circular_dependency(self):
        driver = self.driver

        # -------- Login with invalid email ----------
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        email_input.clear()
        email_input.send_keys("invalidemail.com")  # Missing "@"
        password_input.clear()
        password_input.send_keys("abc123")
        time.sleep(1)
        login_button.click()
        time.sleep(2)

        # HTML5 input should block submission
        self.assertNotEqual(email_input.get_attribute("validationMessage"), "")

        # -------- Login with valid email ----------
        email_input.clear()
        email_input.send_keys("test@example.com")
        login_button.click()
        time.sleep(4)

        # -------- Go to Survey Builder ----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        # -------- Add Q1: Do you exercise? ----------
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.clear()
        label_input.send_keys("Do you exercise?")
        time.sleep(1)

        # Select Multiple Choice
        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        time.sleep(0.5)
        type_dropdown.find_element(By.XPATH, ".//option[@value='multiple_choice']").click()
        time.sleep(1)

        # Add Option 1: Yes
        option_0 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']")
        option_0.clear()
        option_0.send_keys("Yes")
        time.sleep(1)

        # Add another option
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        time.sleep(1)

        # Add Option 2: No
        option_1 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']")
        option_1.clear()
        option_1.send_keys("No")
        time.sleep(1)

        # Submit the question
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # -------- Add Q2: How often? (depends on Q1 = Yes) ----------
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("How often?")
        type_dropdown = Select(driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']"))
        type_dropdown.select_by_value("multiple_choice")
        time.sleep(1)

        # Add Option 1: Daily
        option_0 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']")
        option_0.clear()
        option_0.send_keys("Daily")
        time.sleep(1)
        
        # Add Option 2: Weekly
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        option_1 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']")
        option_1.clear()
        option_1.send_keys("Weekly")
        time.sleep(1)

        # Open condition select dropdown
        condition_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']")
        condition_dropdown.click()
        time.sleep(0.5)

        # Select dependent question: "Do you exercise?"
        # Open condition select
        dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']")
        dropdown.click()
        time.sleep(0.5)

        # Click the dependent question option: Do you exercise?
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-do-you-exercise?']").click()
        time.sleep(1)

        # Click the matching answer radio (e.g., Yes, Daily, etc.)
        driver.find_element(By.XPATH, "//label[contains(text(), 'Yes')]/input[@type='radio']").click()
        time.sleep(2)


        # -------- Edit Q1 to depend on Q2 (circular) ----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Edit')]").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-how-often?']").click()
        driver.find_element(By.XPATH, "//label[contains(text(), 'Daily')]/input").click()
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
