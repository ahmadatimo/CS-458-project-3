from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase10(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(3)

    def test_email_format_and_missing_condition_answer(self):
        driver = self.driver

        # ---------- Login with invalid email ----------
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        email_input.clear()
        email_input.send_keys("user@example")  # missing "@"
        password_input.clear()
        password_input.send_keys("abc123")
        time.sleep(1)
        login_button.click()
        time.sleep(2)

        # Retry with valid credentials
        email_input.clear()
        email_input.send_keys("test@example.com")
        time.sleep(0.5)
        login_button.click()
        time.sleep(4)

        # ---------- Navigate to Survey Builder ----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(3)

        # ---------- Add Q1: Do you own a pet? ----------
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.clear()
        label_input.send_keys("Do you own a pet?")
        time.sleep(1)

        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        time.sleep(0.5)
        type_dropdown.find_element(By.XPATH, ".//option[@value='dropdown']").click()
        time.sleep(1)

        option_0 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']")
        option_0.send_keys("Yes")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        time.sleep(0.5)
        option_1 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']")
        option_1.send_keys("No")
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ---------- Add Q2: Pet type? with condition but no required answer ----------
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.clear()
        label_input.send_keys("Pet type?")
        time.sleep(1)

        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        time.sleep(0.5)
        type_dropdown.find_element(By.XPATH, ".//option[@value='text']").click()
        time.sleep(1)

        # Select dependency but no answer
        condition_select = driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']")
        condition_select.click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-do-you-own-a-pet?']").click()
        time.sleep(1)

        # Try submitting without required answer
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # Expect validation message
        error_msg = driver.find_element(By.ID, "question-error").text
        print("Error message:", error_msg)
        self.assertIn("Please specify the required answer", error_msg)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
