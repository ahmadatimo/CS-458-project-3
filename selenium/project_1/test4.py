from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Create a WebDriver service macOS/linux Version
#service = Service(executable_path="/Users/(Name of user)/Desktop/Git/git/Project/CS-458-project/selenium/project_1/chromedriver")

# Create a WebDriver service Windows Version
service = Service(executable_path="chromedriver.exe")

# Start Chrome WebDriver with the service
driver = webdriver.Chrome(service=service)  # ✅ 'service' should be lowercase

# Open the frontend (Vite default port)
driver.get("http://localhost:3000")

time.sleep(2)

# Click spotify_button:
Spotify_Button = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/button').click()
time.sleep(2)

# assign elements
Spotify_Email = driver.find_element(By.XPATH, '//*[@id="login-username"]')
Spotify_Password = driver.find_element(By.XPATH, '//*[@id="login-password"]')
Spotify_login = driver.find_element(By.XPATH, '//*[@id="login-button"]/span[1]')

Spotify_Email.send_keys("cs458@gmail.com")
time.sleep(2)

Spotify_Password.send_keys("CS458Tests12345")
time.sleep(2)

Spotify_login.click()
time.sleep(2)

Spotify_Email.clear()
time.sleep(2)

Spotify_Email.send_keys("cs458tests@gmail.com")
time.sleep(2)

Spotify_login.click()
time.sleep(2)

driver.quit()

