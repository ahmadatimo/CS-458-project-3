from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase16(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(2)

    def test_whitespace_email_and_max_question_limit(self):
        driver = self.driver

        # ----------- Login with whitespace in email -----------
        email = driver.find_element(By.ID, "email")
        password = driver.find_element(By.ID, "password")
        email.clear()
        email.send_keys("   test@example.com   ")  # Whitespace around
        password.clear()
        password.send_keys("abc123")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        # ----------- Go to Create Survey -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        # ----------- Add 11 Questions -----------
        for i in range(11):
            label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
            label_input.clear()
            label_input.send_keys(f"Question {i+1}")
            time.sleep(0.5)

            type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
            type_dropdown.click()
            type_dropdown.find_element(By.XPATH, ".//option[@value='text']").click()
            time.sleep(0.5)

            driver.find_element(By.ID, "add-question-button").click()
            time.sleep(0.8)

        # ----------- Check for error message (Max limit) -----------
        try:
            error = driver.find_element(By.ID, "question-error")
            assert "10" in error.text.lower() or "maximum" in error.text.lower()
            print("✅ Max question limit enforced: ", error.text)
        except:
            print("❌ Max question limit not enforced or error message missing.")
            self.fail("11th question added without restriction.")

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
