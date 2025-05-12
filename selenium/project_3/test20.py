from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase20(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(2)

    def test_password_special_characters_and_email_validation(self):
        driver = self.driver

        # ----------- PART 1: Special Characters Only Password -----------
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        email_field.send_keys("test@example.com")
        password_field.send_keys("@!#$%^&*()")
        login_button.click()
        time.sleep(2)


        # ----------- Valid Login After Invalid Attempt -----------
        email_field.clear()
        password_field = driver.find_element(By.ID, "password")

        # Clear using JS to ensure total reset
        driver.execute_script("arguments[0].value = '';", password_field)
        password_field.clear()  # fallback
        password_field.send_keys("abc123")
        login_button.click()
        time.sleep(3)

        # ----------- Navigate to Survey Builder + Create Survey -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        # Q1 (Independent): Favorite animal?
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Favorite animal?")
        dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        dropdown.click()
        dropdown.find_element(By.XPATH, ".//option[@value='dropdown']").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Dog")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("Cat")
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # Q2 (Dependent): Why do you like them?
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Why do you like them?")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-favorite-animal?']").click()
        driver.find_element(By.XPATH, "//label[contains(text(), 'Dog')]/input").click()
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Go to Fill Survey Page -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(2)

        # ----------- Email Validation Testing in Fill Survey Page -----------
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")

        # Step 1: No email
        assert not submit_button.is_enabled()
        print("✅ Submit is disabled with no email.")

        # Step 2: Invalid email
        email_input.send_keys("user@domain")
        time.sleep(3)
        assert not submit_button.is_enabled()
        print("✅ Submit remains disabled for invalid email.")

        # Step 3: Valid email
        email_input.clear()
        email_input.send_keys("test@example.com")
        time.sleep(1)
        assert submit_button.is_enabled()
        print("✅ Submit is enabled with valid email.")

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
