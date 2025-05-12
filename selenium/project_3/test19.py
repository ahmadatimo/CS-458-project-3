from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase19(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(2)

    def test_duplicate_question_detection(self):
        driver = self.driver

        # ----------- Login -----------
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        email_field.send_keys("test@example.com")
        password_field.send_keys("abc123")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        # ----------- Create Survey -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        # ----------- Add Question: Favorite color? (Dropdown: Red, Blue, Green) -----------
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Favorite color?")
        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        type_dropdown.find_element(By.XPATH, ".//option[@value='dropdown']").click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Red")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("Blue")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-2']").send_keys("Green")
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Try to Add Identical Question Again -----------
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Favorite color?")
        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        type_dropdown.find_element(By.XPATH, ".//option[@value='dropdown']").click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Red")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("Blue")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-2']").send_keys("Green")
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Check for warning about duplicate -----------
        error_elements = driver.find_elements(By.ID, "question-error")
        assert any("already exists" in e.text.lower() for e in error_elements), "❌ No duplicate warning shown"
        print("✅ Duplicate question warning displayed as expected.")

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
