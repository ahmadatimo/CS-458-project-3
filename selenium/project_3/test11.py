from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest
import os # Added for creating screenshots directory

class TestCase11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        # Optional: Add a common user-agent to appear like a regular browser
        # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.maximize_window()

        # Create a directory for screenshots if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
            print("Created 'screenshots' directory.")

    def save_debug_screenshot(self, name_prefix):
        """Helper function to save screenshots with a timestamp."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshots/{name_prefix}_{timestamp}.png"
        try:
            self.driver.save_screenshot(filename)
            print(f"Saved screenshot: {filename}")
            print(f"Current URL at screenshot: {self.driver.current_url}")
            # Optionally save page source for deep debugging:
            # source_filename = f"screenshots/{name_prefix}_{timestamp}.html"
            # with open(source_filename, "w", encoding="utf-8") as f:
            #     f.write(self.driver.page_source)
            # print(f"Saved page source: {source_filename}")
        except Exception as e:
            print(f"Could not save screenshot or page source: {e}")


    def test_spotify_login_and_dependency_break(self):
        driver = self.driver
        driver.get("http://localhost:3000") # Assuming this is your app
        time.sleep(2)
        # Click your app's "Login with Spotify" button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login with Spotify')]"))
        ).click()

        # Wait for Spotify's login page to load
        try:
            WebDriverWait(driver, 15).until(
                EC.url_contains("accounts.spotify.com") # Or "spotify.com/login" or other patterns
            )
            print("Redirected to Spotify login page.")
        except Exception as e:
            self.save_debug_screenshot("spotify_redirect_fail")
            self.fail(f"Failed to redirect to Spotify login page: {e}")


        # ----------- Spotify Login Logic ------------
        try:
            # Wait for the email field to be present and enter email
            email_field = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "login-username"))
            )
            email_field.clear()
            email_field.send_keys("cs458tests@gmail.com") # Replace with your actual test email if different
            print("Entered email.")
            time.sleep(0.5) # Short pause after typing

            # STEP 1: Check if password field is already visible (ideal scenario)
            try:
                driver.find_element(By.ID, "login-password")
                print("Password field is already visible. Proceeding to enter password.")
                # If found, the script will naturally proceed to STEP 4 logic for password entry
            except:
                # Password field not immediately visible, try other steps
                print("Password field not immediately visible. Attempting to find password login option...")
                self.save_debug_screenshot("after_email_entry_no_pw_field")

                # STEP 2: Try to click a "Next" or "Continue" button if it exists.
                clicked_next_button = False
                try:
                    next_button_xpaths = [
                        "//button[@type='submit' and (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'next'))]",
                        "//button[@type='submit' and (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue'))]",
                        "//button[normalize-space()='Next']",
                        "//button[normalize-space()='Continue']",
                        # A general login button if it acts as next (e.g. has 'login-button' testid but not 'login-button' id, and no password field present)
                        "//button[@data-testid='login-button' and not(@id='login-button') and not(ancestor-or-self::form//input[@id='login-password'])]"
                    ]
                    for xpath_idx, xpath in enumerate(next_button_xpaths):
                        print(f"Attempting to find 'Next/Continue' button with XPath #{xpath_idx+1}: {xpath}")
                        try:
                            next_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                            print(f"Found 'Next/Continue' button. Clicking it.")
                            next_button.click()
                            clicked_next_button = True
                            WebDriverWait(driver, 7).until(lambda d: d.execute_script('return document.readyState') == 'complete')
                            time.sleep(1.5) # UI settle
                            self.save_debug_screenshot("after_clicking_next_button")
                            break
                        except:
                            # print(f"XPath #{xpath_idx+1} for 'Next/Continue' not found or clickable.")
                            continue
                    if not clicked_next_button:
                         print("No distinct 'Next' or 'Continue' button found or clicked after email.")

                except Exception as e_next:
                    print(f"Error attempting to click 'Next/Continue' button: {e_next}")
                    self.save_debug_screenshot("error_clicking_next_button")

                # STEP 3: Now, specifically look for an option to use password.
                found_and_clicked_password_option = False
                try:
                    # PRIORITIZED XPaths based on your provided HTML:
                    password_option_xpaths = [
                        "//button[@data-encore-id='buttonTertiary' and normalize-space(text())='Log in with a password']",
                        "//button[@data-encore-id='buttonTertiary']", # If text is tricky but ID is solid
                        "//button[contains(@class, 'Button-sc-1dqy6lx-0') and contains(@class, 'jmTWwm') and normalize-space(text())='Log in with a password']",
                        # Fallback: Original more generic XPaths
                        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'log in with password')]",
                        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'use your password')]",
                        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'use password instead')]",
                        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'try another way')]", # "Try another way" sometimes leads to password
                        "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'log in with password')]",
                        "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'use your password')]",
                        "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'use password instead')]",
                        "//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'try another way')]"
                    ]
                    print("Searching for 'Log in with password' or similar options (prioritizing specific selectors)...")
                    for xpath_idx, xpath in enumerate(password_option_xpaths):
                        print(f"Attempting XPath #{xpath_idx + 1} for password option: {xpath}")
                        try:
                            password_option_elements = WebDriverWait(driver, 4).until( # Slightly shorter wait per XPath
                                EC.presence_of_all_elements_located((By.XPATH, xpath))
                            )
                            if password_option_elements:
                                print(f"Found {len(password_option_elements)} element(s) with current XPath.")
                                for elem_idx, elem in enumerate(password_option_elements):
                                    print(f"Checking element #{elem_idx+1} (XPath #{xpath_idx+1})...")
                                    try:
                                        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", elem)
                                        time.sleep(0.3)
                                        if WebDriverWait(driver, 2).until(EC.visibility_of(elem)) and elem.is_enabled():
                                            print(f"Element '{elem.text}' is visible and enabled. Attempting click...")
                                            driver.execute_script("arguments[0].click();", elem)
                                            print(f"Clicked element '{elem.text}' (XPath: {xpath})")
                                            WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "login-password")))
                                            print("Password field appeared after clicking password option.")
                                            found_and_clicked_password_option = True
                                            self.save_debug_screenshot("password_option_clicked_successfully")
                                            break
                                        else:
                                            print(f"Element '{elem.text}' found but not visible/enabled.")
                                    except Exception as e_click_option:
                                        print(f"Could not click or verify password option element '{elem.text}' (XPath: {xpath}, Element Index: {elem_idx}): {e_click_option}")
                                        self.save_debug_screenshot(f"pw_opt_click_fail_xpath{xpath_idx}_elem{elem_idx}")
                                if found_and_clicked_password_option:
                                    break
                        except: # TimeoutException or other for this specific XPath
                            # print(f"No elements found or other error for XPath #{xpath_idx + 1}")
                            if xpath_idx == 0: # If the most specific one (data-encore-id) failed
                                self.save_debug_screenshot("specific_encore_id_button_xpath_failed")
                            continue
                    if not found_and_clicked_password_option:
                        print("Could NOT find and click any explicit option to log in with a password after trying all XPaths.")
                        self.save_debug_screenshot("no_password_option_found_at_all")
                except Exception as e_pw_option:
                    print(f"General error during 'Log in with password' option search: {e_pw_option}")
                    self.save_debug_screenshot("error_finding_password_option_general")

            # STEP 4: Attempt to find and fill the password field
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "login-password"))
            )
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "login-password"))
            )
            password_field.clear()
            password_field.send_keys("CS458Testsssssssss12345")
            time.sleep(1)
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "login-button"))
            )
            login_button.click()
            time.sleep(1)
            password_field.clear()
            password_field.send_keys("CS458Tests12345") # Replace with your actual test password if different
            print("Entered password.")
            time.sleep(1)

            login_button.click()
            print("Clicked final login button.")

            WebDriverWait(driver, 20).until(
                lambda d: "localhost:3000" in d.current_url or \
                          "spotify.com/us/home" in d.current_url or \
                          "open.spotify.com" in d.current_url # Common Spotify dashboard/app URLs
            )
            print("Login appears successful. Current URL:", driver.current_url)

        except Exception as e:
            print(f"Spotify login failed: {e}")
            self.save_debug_screenshot("spotify_login_final_fail")
            self.fail(f"Spotify login failed: {e}")

        # ----------- Create Survey Flow (Your existing code) ------------
        driver.get("http://localhost:3000/Survey")
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create Survey')]"))
        ).click()
        time.sleep(2)

        # ----------- Q1: Use AI tools? ------------
        label = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='question-label']")))
        label.clear()
        label.send_keys("Use AI tools?")
        dropdown = driver.find_element(By.CSS_SELECTOR, "[data-testid='question-type']")
        dropdown.click()
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, ".//option[@value='multiple_choice']"))).click()
        time.sleep(1) # Allow UI to update
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-0']").send_keys("Yes")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='add-option-button']").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "[data-testid='option-input-1']").send_keys("No")
        time.sleep(1)
        driver.find_element(By.ID, "add-question-button").click()
        time.sleep(2)

        # ----------- Q2: Which tools? depends on Q1 = Yes ------------
        # Assuming a new question form appears, re-locate elements
        question_labels = driver.find_elements(By.CSS_SELECTOR, "[data-testid='question-label']")
        # Target the new (likely the last or second if they persist) question label
        new_q_label = question_labels[-1] if len(question_labels) > 1 else question_labels[0]
        new_q_label.send_keys("Which tools?")

        question_types = driver.find_elements(By.CSS_SELECTOR, "[data-testid='question-type']")
        new_q_type_dropdown = question_types[-1] if len(question_types) > 1 else question_types[0]
        new_q_type_dropdown.click()
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//select[@data-testid='question-type']/option[@value='text']"))).click()

        condition_selects = driver.find_elements(By.CSS_SELECTOR, "[data-testid='condition-select']")
        new_q_condition_select = condition_selects[-1] if len(condition_selects) > 1 else condition_selects[0]
        new_q_condition_select.click()
        time.sleep(1) # For dropdown options to appear
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='condition-option-use-ai-tools?']"))).click()
        time.sleep(1)
        # Assuming radio button for "Yes" is within the context of the last question added or specific to it
        # This XPath might need to be more specific if there are multiple "Yes" options on the page
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Yes')]/input[@type='radio']"))).click()
        time.sleep(1)

        add_question_buttons = driver.find_elements(By.ID, "add-question-button")
        add_question_buttons[-1].click() # Click the relevant "add question" button for the current question
        time.sleep(2)

        # ----------- Delete Q1 ------------
        # Be careful with indexing if questions can be reordered or if the structure changes
        delete_buttons = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), '🗑️ Delete')]")))
        if delete_buttons:
            delete_buttons[0].click() # Deletes the first question
            time.sleep(1)
        else:
            print("No delete buttons found.")


        # ----------- Verify condition behavior ------------
        alerts = driver.find_elements(By.ID, "question-error") # This ID might be too generic
        # It's better to find alerts related to the specific question that had its dependency broken.
        # This part may need more specific selectors based on your application's HTML structure for errors.
        if alerts:
            print("⚠️ Alert shown:", alerts[0].text) # Assuming the first alert is relevant
        else:
            print("✅ Q2's condition was auto-cleared or handled gracefully (or no alert with that ID found).")


    @classmethod
    def tearDownClass(cls):
        time.sleep(2) # Observe final state
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()