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
driver = webdriver.Chrome(service=service) 

# Open the frontend (Vite default port)
driver.get("http://localhost:3000")

# appreciate the page
time.sleep(1)

# identify the elements
email = driver.find_element(By.NAME, "email")
password = driver.find_element(By.NAME, "password")
login = driver.find_element(By.NAME, "submit")

time.sleep(1)

# log in with an empty email & password
login.send_keys(Keys.ENTER)
time.sleep(2)

# add an email
email.send_keys("lupin@hogwarts.com")
login.send_keys(Keys.ENTER)
time.sleep(2)

# add a password
password.send_keys("eatCh0klate")
email.clear()
login.send_keys(Keys.ENTER)
time.sleep(2)

# log in finally
email.send_keys("lupin@hogwarts.com")
password.clear()
password.send_keys("eatCh0klate")
login.send_keys(Keys.ENTER)
time.sleep(3)

# Close the browser
driver.quit()
