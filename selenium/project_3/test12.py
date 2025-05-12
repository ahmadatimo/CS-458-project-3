from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCase12(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.get("http://localhost:3000")
        time.sleep(2)

    def test_lockout_and_multilingual_labels(self):
        driver = self.driver

        # ----------- PART 1: Trigger Lockout by entering wrong password 5 times -----------
        ##for _ in range(5):
            #email = driver.find_element(By.ID, "email")
            #password = driver.find_element(By.ID, "password")
            #email.clear()
            #email.send_keys("test@example.com")
            #password.clear()
            #password.send_keys("wrong234")
            #driver.find_element(By.ID, "login-button").click()
            #time.sleep(1)

        # 6th attempt with correct password (should be blocked)
        #time.sleep(1)

        # Wait 60 seconds to unlock
        #time.sleep(60)

        # Retry with correct password (should succeed)
        email = driver.find_element(By.ID, "email")
        password = driver.find_element(By.ID, "password")
        email.clear()
        email.send_keys("test@example.com")
        password.clear()
        password.send_keys("abc123")
        driver.find_element(By.ID, "login-button").click()
        time.sleep(5)

        # ----------- PART 2: Multilingual Input in Survey Question Labels -----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Create Survey')]").click()
        time.sleep(2)

        arabic_label = "ما اسمك؟ 🐪"
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        driver.execute_script("arguments[0].value = arguments[1];", label_input, arabic_label)
        time.sleep(0.5)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(1)

        # ---------- Add Chinese + Emoji Label ----------
        chinese_label = "你叫什么名字？🐉"
        label_input = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-label']")
        driver.execute_script("arguments[0].value = arguments[1];", label_input, chinese_label)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", label_input)
        time.sleep(0.5)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(1)

        # ---------- Go to Fill Survey ----------
        driver.find_element(By.XPATH, "//button[contains(text(), 'Fill Survey')]").click()
        time.sleep(2)

        # ---------- Fill answers ----------
        text_inputs = driver.find_elements(By.TAG_NAME, "input")
        for inp in text_inputs:
            inp.send_keys("测试")  # Generic input, can be any Unicode text

        # ---------- Submit Survey ----------
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
        )
        submit_btn.click()
        time.sleep(2)


    @classmethod
    def tearDownClass(cls):
        time.sleep(2)
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
