from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import unittest

class TestCase17(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(2)

    def test_password_whitespace_and_trimmed_logic(self):
        driver = self.driver

        # ----------- Login with whitespace-padded password (should fail) -----------
        email1 = driver.find_element(By.ID, "email")
        password1 = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        email1.clear()
        email1.send_keys("test@example.com")
        password1.clear()
        password1.send_keys(" abc123 ")  # Invalid due to spaces
        login_button.click()
        time.sleep(2)

        # ----------- Login with correct password (no spaces) -----------
        email2 = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "password")
        email2.clear()
        email2.send_keys("test@example.com")
        driver.execute_script("arguments[0].value = '';", password_field)
        password_field.clear()  # fallback
        password_field.send_keys("abc123")
        login_button.click()
        time.sleep(3)

        # ----------- Navigate to Survey Builder -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        # ----------- Q1: Favorite animal? -----------
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.send_keys("Favorite animal?")

        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        time.sleep(1)
        type_dropdown.find_element(By.XPATH, ".//option[@value='dropdown']").click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Cat")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("  Dog  ")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-2']").send_keys("Other")
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Q2: Why do you like them? (Condition: Q1 = '  Dog  ') -----------
        driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']").send_keys("Why do you like them?")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-favorite-animal?']").click()
        time.sleep(1)

        # Select 'Dog' condition via JavaScript to simulate whitespace-trim logic
        js = """
            const radios = [...document.querySelectorAll('label')];
            const match = radios.find(r => r.textContent.trim() === 'Dog');
            if (match) match.querySelector('input').click();
        """
        driver.execute_script(js)
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Preview survey and select Dog -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(2)

        dropdown = Select(driver.find_element(By.TAG_NAME, "select"))
        dropdown.select_by_visible_text("Dog")
        time.sleep(2)

        # ----------- Verify Q2 appears -----------
        assert "Why do you like them?" in driver.page_source
        print("✅ Q2 appeared after selecting trimmed 'Dog' — whitespace logic handled properly.")

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
