from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase6(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(3)

    def test_numeric_password_and_model_deselection(self):
        driver = self.driver

        # ----------- Part 1: Login Page ------------

        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")

        email_input.clear()
        email_input.send_keys("test@example.com")
        time.sleep(1)

        # Password = numbers only
        password_input.clear()
        password_input.send_keys("123456")
        time.sleep(1)
        login_button.click()
        time.sleep(2)

        # Valid login
        password_input.clear()
        password_input.send_keys("abc123")
        time.sleep(1)
        login_button.click()
        time.sleep(5)

        # ----------- Part 2: Survey Page ------------

        driver.find_element(By.ID, "name_surname").send_keys("Lily Evans")
        time.sleep(1)
        driver.find_element(By.ID, "birth_day").send_keys("25")
        driver.find_element(By.ID, "birth_month").send_keys("7")
        driver.find_element(By.ID, "birth_year").send_keys("1990")
        time.sleep(1)
        driver.find_element(By.ID, "education_level").send_keys("Undergraduate")
        driver.find_element(By.ID, "city").send_keys("Godric's Hollow")
        driver.find_element(By.ID, "gender-female").click()
        time.sleep(1)

        # Select ChatGPT and Bard
        chatgpt_btn = driver.find_element(By.ID, "model-ChatGPT")
        bard_btn = driver.find_element(By.ID, "model-Bard")

        chatgpt_btn.click()
        time.sleep(1)
        bard_btn.click()
        time.sleep(2)

        # Check both defect fields exist
        defect_chatgpt = driver.find_element(By.ID, "defect-ChatGPT")
        defect_bard = driver.find_element(By.ID, "defect-Bard")

        defect_chatgpt.send_keys("ChatGPT defect.")
        defect_bard.send_keys("Bard defect.")
        time.sleep(2)

        # Deselect Bard
        bard_btn.click()
        time.sleep(2)

        # Bard field should now be gone
        bard_defect_fields = driver.find_elements(By.ID, "defect-Bard")
        self.assertEqual(len(bard_defect_fields), 0)
        time.sleep(1)

        # ChatGPT field should still exist with value intact
        remaining_chatgpt = driver.find_element(By.ID, "defect-ChatGPT")
        self.assertEqual(remaining_chatgpt.get_attribute("value"), "ChatGPT defect.")
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
