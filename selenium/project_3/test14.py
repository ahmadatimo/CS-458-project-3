from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class TestCase14(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(3)

    def test_dynamic_type_switch_and_data_persistence(self):
        driver = self.driver

        # ----------- Login -----------
        driver.find_element(By.ID, "email").send_keys("test@example.com")
        driver.find_element(By.ID, "password").send_keys("abc123")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(3)

        # ----------- Navigate to Create Survey -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        # ----------- Create a Dropdown Question First -----------
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.send_keys("Favorite colors?")
        time.sleep(1)

        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        type_dropdown.find_element(By.XPATH, ".//option[@value='dropdown']").click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Red")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("Green")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-2']").send_keys("Blue")
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Edit and Switch to Multiple Choice -----------
        edit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Edit')]")
        edit_button.click()
        time.sleep(1)

        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        type_dropdown.find_element(By.XPATH, ".//option[@value='multiple_choice']").click()
        time.sleep(1)

        # ----------- Then Switch to Checkbox -----------
        type_dropdown.click()
        type_dropdown.find_element(By.XPATH, ".//option[@value='checkbox']").click()
        time.sleep(1)

        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Go to Fill Survey -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(2)

        # ----------- Validate that options still appear -----------
        dropdown = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//select"))
        )
        Select(dropdown).select_by_visible_text("Green")
        selected_option = dropdown.get_attribute("value")
        assert selected_option == "Green" or "green" in selected_option.lower()
        print("✅ Successfully selected 'Green' from dropdown after type switches.")

    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
