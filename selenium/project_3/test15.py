from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase15(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(2)

    def test_condition_removal_behavior(self):
        driver = self.driver

        # ----------- Login -----------
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("abc123")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        # ----------- Create Survey -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        # ----------- Q1: Use AI tools? -----------
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Use AI tools?")
        dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        dropdown.click()
        dropdown.find_element(By.XPATH, ".//option[@value='multiple_choice']").click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Yes")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("No")
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Q2: Which one? (Condition: Q1 = Yes) -----------
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Which one?")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-use-ai-tools?']").click()
        driver.find_element(By.XPATH, "//label[contains(text(), 'Yes')]/input").click()
        time.sleep(1)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Edit Q2 and remove its condition -----------
        edit_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Edit')]")
        edit_buttons[1].click()  # Edit Q2 (the second question)
        time.sleep(1)

        condition_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']")
        condition_dropdown.click()
        time.sleep(0.5)

        # Select "no condition" (empty value)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select'] > option[value='']").click()
        time.sleep(1)

        # Update the question
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Fill Survey -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(2)

        # Assert that both Q1 and Q2 are visible without conditions
        page = driver.page_source
        assert "Use AI tools?" in page
        assert "Which one?" in page
        print("✅ Q2 is now unconditional and visible as expected.")

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
