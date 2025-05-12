# Modified version of Test Case 13 with more time between actions for easier human-following

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase13(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(3)

    def test_multiple_dependencies(self):
        driver = self.driver

        # ----------- Invalid Login Attempt -----------
        email = driver.find_element(By.ID, "email")
        password = driver.find_element(By.ID, "password")
        email.clear()
        password.clear()
        email.send_keys("test@example.com")
        password.send_keys("wrongpass")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        # ----------- Valid Login Attempt -----------
        password.clear()
        password.send_keys("abc123")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(5)

        # ----------- Navigate to Survey Builder -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(4)

        # ----------- Q1: Do you work remotely? -----------
        label = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label.send_keys("Do you work remotely?")
        time.sleep(2)
        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        time.sleep(1)
        type_dropdown.find_element(By.XPATH, ".//option[@value='multiple_choice']").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Yes")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("No")
        time.sleep(1)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(3)

        # ----------- Q2: Working hours? (Q1 = Yes) -----------
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Working hours?")
        time.sleep(1)
        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        time.sleep(1)
        type_dropdown.find_element(By.XPATH, ".//option[@value='text']").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-do-you-work-remotely?']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//label[contains(text(), 'Yes')]/input").click()
        time.sleep(1)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(3)

        # ----------- Q3: Work location preference? (Q1 = Yes) -----------
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Work location preference?")
        time.sleep(1)
        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        time.sleep(1)
        type_dropdown.find_element(By.XPATH, ".//option[@value='text']").click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-do-you-work-remotely?']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//label[contains(text(), 'Yes')]/input").click()
        time.sleep(1)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(4)

        # ----------- Fill Survey Preview -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(4)

        # ----------- Select Q1 = Yes to trigger Q2 & Q3 -----------
        driver.find_element(By.XPATH, "//label[contains(text(), 'Yes')]/input").click()
        time.sleep(3)

        # Check both Q2 and Q3 appear
        page_source = driver.page_source
        self.assertIn("Working hours?", page_source)
        self.assertIn("Work location preference?", page_source)

        # Switch to Q1 = No and make sure Q2 & Q3 disappear
        driver.find_element(By.XPATH, "//label[contains(text(), 'No')]/input").click()
        time.sleep(3)
        self.assertNotIn("Working hours?", driver.page_source)
        self.assertNotIn("Work location preference?", driver.page_source)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
