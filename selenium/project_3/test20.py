from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class TestCaseEmailAndAnswers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        print("🌐 Opened the application.")
        time.sleep(3)

    def test_submit_requires_valid_email_and_answers(self):
        driver = self.driver

        # ----------- Attempt with special character password (should fail) -----------
        # ----------- Attempt with special character password (should fail) -----------
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        email_field.send_keys("test@example.com")
        # ----------- Enter special character password (should fail) -----------
        password_field = driver.find_element(By.ID, "password")
        driver.execute_script("arguments[0].value = '';", password_field)
        password_field.send_keys("@!#$%^&*()")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # ----------- Now enter correct password (after JS clear) -----------
        print("\n🔐 Retrying with correct password...")
        password_field = driver.find_element(By.ID, "password")
        driver.execute_script("arguments[0].value = '';", password_field)  # Clear using JS
        password_field.send_keys("abc123")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        # ----------- Go to Survey Builder -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(3)

        # ----------- Q1: Favorite animal? -----------
        print("➕ Adding Q1: Favorite animal?")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Favorite animal?")
        dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        dropdown.click()
        time.sleep(1.5)
        dropdown.find_element(By.XPATH, ".//option[@value='dropdown']").click()
        time.sleep(1.5)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Dog")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("Cat")
        time.sleep(1)
        driver.find_element(By.ID, "add-question-button").click()
        print("✅ Q1 added.")
        time.sleep(3)

        # ----------- Q2: Why do you like them? (Dependent on Q1 = Dog) -----------
        print("➕ Adding Q2: Why do you like them? (dependent on Q1 = Dog)")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Why do you like them?")
        time.sleep(1.5)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-favorite-animal?']").click()
        time.sleep(1.5)
        driver.find_element(By.XPATH, "//label[contains(text(), 'Dog')]/input").click()
        time.sleep(1.5)
        driver.find_element(By.ID, "add-question-button").click()
        print("✅ Q2 added.")
        time.sleep(3)

        # ----------- Go to Fill Survey Page -----------
        print("🧪 Navigating to Fill Survey page...")
        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(3)

        # ----------- Email Validation Tests -----------
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")

        print("❌ Trying to submit without email...")
        assert not submit_button.is_enabled()
        print("✔️ Submit is disabled with no email.")
        time.sleep(2.5)

        print("❌ Trying to submit with valid email but no answers...")
        email_input.clear()
        email_input.send_keys("test@example.com")
        time.sleep(2)
        assert not submit_button.is_enabled()
        print("✔️ Submit remains disabled without answering questions.")
        time.sleep(2)

        # ----------- Answer Q1 to trigger Q2 -----------
        print("📝 Answering Q1: Selecting Dog...")
        dropdown_q1 = driver.find_element(By.TAG_NAME, "select")
        Select(dropdown_q1).select_by_visible_text("Dog")
        time.sleep(3)

        # ----------- Answer Q2 now that it's visible -----------
        print("📝 Answering Q2: Typing reason...")
        textarea = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        textarea.send_keys("Because they are loyal.")
        time.sleep(2)

        # ----------- Now check submit enabled -----------
        print("✅ All fields completed. Checking submit button...")
        assert submit_button.is_enabled()
        print("🎉 Submit is enabled after valid email + all answers.")

    @classmethod
    def tearDownClass(cls):
        print("\n🧹 Test complete. Closing browser...")
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
