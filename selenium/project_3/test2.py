from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")  # Adjust if needed
        time.sleep(3)  # Wait for page to load

    def test_empty_email_and_multiple_ai_models(self):
        driver = self.driver

        # ----------- Part 1: Login Page ------------

        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.ID, "login-button")

        # 1. Empty email
        email_input.clear()
        time.sleep(1)
        password_input.send_keys("abc123")
        time.sleep(1)
        login_button.click()
        time.sleep(3)

        # Reload login page for clean state
        driver.get("http://localhost:3000/login")
        time.sleep(3)

        # 2. Valid login
        driver.find_element(By.NAME, "email").send_keys("test@example.com")
        time.sleep(1)
        driver.find_element(By.NAME, "password").send_keys("abc123")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(4)

        self.assertIn("AI Usage Survey", driver.page_source)

        # ----------- Part 2: Survey Page ------------

        driver.find_element(By.ID, "name_surname").send_keys("John Doe")
        time.sleep(1)
        driver.find_element(By.ID, "birth_day").send_keys("12")
        time.sleep(1)
        driver.find_element(By.ID, "birth_month").send_keys("6")
        time.sleep(1)
        driver.find_element(By.ID, "birth_year").send_keys("1998")
        time.sleep(1)
        driver.find_element(By.ID, "education_level").send_keys("Undergraduate")
        time.sleep(1)
        driver.find_element(By.ID, "city").send_keys("Istanbul")
        time.sleep(1)
        driver.find_element(By.ID, "gender-female").click()
        time.sleep(1)
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        time.sleep(1)
        driver.find_element(By.ID, "beneficial_use").send_keys("Research and productivity.")
        time.sleep(2)

        # Select AI models
        driver.find_element(By.ID, "model-ChatGPT").click()
        time.sleep(1)
        driver.find_element(By.ID, "model-Bard").click()
        time.sleep(2)

        # Enter different defects
        defect_chatgpt = driver.find_element(By.ID, "defect-ChatGPT")
        defect_bard = driver.find_element(By.ID, "defect-Bard")

        defect_chatgpt.send_keys("Sometimes fabricates sources.")
        time.sleep(2)
        defect_bard.send_keys("Not always up to date.")
        time.sleep(2)

        # Verify both inputs retain their values
        self.assertEqual(defect_chatgpt.get_attribute("value"), "Sometimes fabricates sources.")
        self.assertEqual(defect_bard.get_attribute("value"), "Not always up to date.")

        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
