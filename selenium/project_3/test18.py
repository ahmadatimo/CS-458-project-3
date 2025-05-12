from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase18(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(2)

    def test_whitespace_password_and_case_insensitive_logic(self):
        driver = self.driver

        # ----------- Attempt login with spaces only as password -----------
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("   ")  # Invalid password
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # ----------- Login with correct password -----------
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")

        email_input.clear()
        password_input.clear()

        email1 = "test@example.com"
        password1 = "abc123"

        email_input.send_keys(email1)
        # Re-find password field to avoid stale reference
        password_field = driver.find_element(By.ID, "password")

        # Clear using JS to ensure total reset
        driver.execute_script("arguments[0].value = '';", password_field)
        password_field.clear()  # fallback
        password_field.send_keys("abc123")

        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        # ----------- Go to Create Survey -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        # ----------- Add Q1: "Type your favorite color" (text) -----------
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.send_keys("Type your favorite color")
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Add Q2: "Nice choice!" depends on Q1 = "blue" -----------
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.send_keys("Nice choice!")
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-type-your-favorite-color']").click()
        time.sleep(1)

        # Free-text input for answer: manually enter "blue" as condition (lowercase)
        cond_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Required answers (comma-separated)']")
        cond_input.clear()
        cond_input.send_keys("blue")
        cond_input.click()  # Blur to trigger onBlur logic
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Preview Survey and Test Case Insensitivity -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(2)

        # Try different capitalizations of "blue"
        test_variants = ["Blue", "BLUE", "bLuE"]
        for variant in test_variants:
            print(f"\n🔍 Trying input: {variant}")
            color_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
            color_input.clear()
            color_input.send_keys(variant)
            time.sleep(1)

            page = driver.page_source
            assert "Nice choice!" in page, f"❌ Failed to show dependent question for input: {variant}"
            print(f"✅ 'Nice choice!' appeared correctly for input: {variant}")

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
