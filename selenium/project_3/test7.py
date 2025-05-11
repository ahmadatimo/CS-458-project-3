from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest

class TestCase7(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(3)

    def test_letters_only_password_and_nested_logic(self):
        driver = self.driver

        # ----------- Login ------------

        driver.find_element(By.ID, "email").send_keys("test@example.com")
        time.sleep(1)
        password = driver.find_element(By.ID, "password")
        password.clear()
        password.send_keys("abcdefghijkl")  # letters only
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # Retry with valid login
        password.clear()
        password.send_keys("abc123")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(5)

        # ----------- Navigate to Survey Builder ------------

        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()

        # Wait for builder page to be fully rendered
        time.sleep(3)

       # ----------- Add Q1: Do you own a pet? ------------

        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.clear()
        label_input.send_keys("Do you own a pet?")
        time.sleep(1)

        # Select Multiple Choice
        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        time.sleep(0.5)
        type_dropdown.find_element(By.XPATH, ".//option[@value='multiple_choice']").click()
        time.sleep(1)

        # Add Option 1: Yes
        option_0 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']")
        option_0.clear()
        option_0.send_keys("Yes")
        time.sleep(1)

        # Add another option
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        time.sleep(1)

        # Add Option 2: No
        option_1 = driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']")
        option_1.clear()
        option_1.send_keys("No")
        time.sleep(1)

        # Submit the question
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Add Q2: Pet type? (Conditional: Q1 = Yes) ------------

        # Type question
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.clear()
        label_input.send_keys("Pet type?")
        time.sleep(1)

        # Select Multiple Choice
        type_dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        type_dropdown.click()
        time.sleep(0.5)
        type_dropdown.find_element(By.XPATH, ".//option[@value='multiple_choice']").click()
        time.sleep(1)

        # Fill options: Dog, Cat, Other
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Dog")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("Cat")
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-2']").send_keys("Other")
        time.sleep(1)

        # Set condition: show if "Do you own a pet?" = "Yes"
        dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']")
        dropdown.click()
        time.sleep(0.5)

        # Click the specific option by test id or visible text
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-do-you-own-a-pet?']").click()

        # Click the "Yes" radio under dependent condition
        driver.find_element(By.XPATH, "//label[contains(text(), 'Yes')]/input[@type='radio']").click()
        time.sleep(1)

        # Add the question
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Add Q3: Specify Type (if Q2 = Other) ------------

        # --- Add Q3: Specify Type (text input) ---

        # 1. Type question label
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        label_input.clear()
        label_input.send_keys("Specify Type")
        time.sleep(1)

        # 2. (Optional) Leave type as "text" — default is text

        # 3. Open dependency dropdown
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-select']").click()
        time.sleep(1)

        # 4. Select Q2 ("Pet type?") as dependency
        driver.find_element(By.CSS_SELECTOR, "[data-testid='condition-option-pet-type?']").click()
        time.sleep(1)

        # 5. Select "Other" option from dependent radio group
        driver.find_element(By.XPATH, "//label[contains(text(), 'Other')]/input[@type='radio']").click()
        time.sleep(1)

        # 6. Add question
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Preview & Fill the Survey ------------

        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(4)

        # Toggle Q1 = Yes → show Q2
        driver.find_element(By.XPATH, "//label[contains(text(), 'Yes')]/input").click()
        time.sleep(2)

        # Toggle Q2 = Other → show Q3
        driver.find_element(By.XPATH, "//label[contains(text(), 'Other')]/input").click()
        time.sleep(2)

        # Toggle Q1 = No → hide Q2 and Q3
        driver.find_element(By.XPATH, "//label[contains(text(), 'No')]/input").click()
        time.sleep(2)

        # Toggle Q1 = Yes → show Q2 again (Q3 hidden unless Other is reselected)
        driver.find_element(By.XPATH, "//label[contains(text(), 'Yes')]/input").click()
        time.sleep(2)
        
        driver.find_element(By.XPATH, "//label[contains(text(), 'Dog')]/input").click()

    @classmethod
    def tearDownClass(cls):
        time.sleep(3)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
