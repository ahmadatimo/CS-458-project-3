from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestCase3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(3)

    def test_empty_login_and_birthdate_validation(self):
        driver = self.driver

        # ----------- Part 1: Login Page ------------

        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        driver.find_element(By.NAME, "email").send_keys("test@example.com")
        time.sleep(1)
        driver.find_element(By.NAME, "password").send_keys("abc123")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(5)

        # ----------- Part 2: Survey Page ------------

        driver.find_element(By.ID, "name_surname").send_keys("Jane Doe")
        time.sleep(1)
        driver.find_element(By.ID, "education_level").send_keys("Undergraduate")
        time.sleep(1)
        driver.find_element(By.ID, "city").send_keys("Izmir")
        time.sleep(1)
        driver.find_element(By.ID, "gender-male").click()
        time.sleep(1)
        driver.find_element(By.ID, "model-ChatGPT").click()
        time.sleep(1)
        driver.find_element(By.ID, "defect-ChatGPT").send_keys("Sometimes inaccurate.")
        time.sleep(1)
        driver.find_element(By.ID, "beneficial_use").send_keys("Learning assistance.")
        time.sleep(1)
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        time.sleep(1)

        submit_button = driver.find_element(By.ID, "submit-button")

        # --- Too Young (<6)
        driver.find_element(By.ID, "birth_day").send_keys("01")
        driver.find_element(By.ID, "birth_month").send_keys("01")
        driver.find_element(By.ID, "birth_year").send_keys("2021")
        time.sleep(2)
        self.assertFalse(submit_button.is_enabled())
        time.sleep(2)

        # --- Too Old (>120)
        driver.find_element(By.ID, "birth_day").clear()
        driver.find_element(By.ID, "birth_month").clear()
        driver.find_element(By.ID, "birth_year").clear()
        time.sleep(1)
        driver.find_element(By.ID, "birth_day").send_keys("01")
        driver.find_element(By.ID, "birth_month").send_keys("01")
        driver.find_element(By.ID, "birth_year").send_keys("1900")
        time.sleep(2)
        self.assertFalse(submit_button.is_enabled())
        time.sleep(2)

        # --- FIXED: Set valid year before testing month overflow
        driver.find_element(By.ID, "birth_day").clear()
        driver.find_element(By.ID, "birth_month").clear()
        driver.find_element(By.ID, "birth_year").clear()
        time.sleep(1)
        driver.find_element(By.ID, "birth_day").send_keys("01")
        driver.find_element(By.ID, "birth_month").send_keys("01")
        driver.find_element(By.ID, "birth_year").send_keys("2010")
        time.sleep(2)

        # --- Invalid month > 12
        driver.find_element(By.ID, "birth_month").clear()
        driver.find_element(By.ID, "birth_month").send_keys("13")
        time.sleep(2)
        self.assertFalse(submit_button.is_enabled())
        time.sleep(2)

        # --- Valid Date
        driver.find_element(By.ID, "birth_day").clear()
        driver.find_element(By.ID, "birth_month").clear()
        driver.find_element(By.ID, "birth_year").clear()
        time.sleep(1)
        driver.find_element(By.ID, "birth_day").send_keys("15")
        driver.find_element(By.ID, "birth_month").send_keys("6")
        driver.find_element(By.ID, "birth_year").send_keys("2000")
        time.sleep(3)

        self.assertTrue(submit_button.is_enabled())
        submit_button.click()
        time.sleep(5)

        self.assertIn("Thank you", driver.page_source)

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
