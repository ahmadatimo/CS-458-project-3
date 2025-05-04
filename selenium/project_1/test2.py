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

# appreciate the page
time.sleep(1)

# assign the elements
email = driver.find_element(By.NAME,"email")
password = driver.find_element(By.NAME, "password")
login = driver.find_element(By.NAME, "submit")

# insert email:
email.send_keys("lupin@hogwarts.com")
time.sleep(1)

# enter short password:
password.send_keys("123")
time.sleep(1)

# submit the first test:
login.send_keys(Keys.ENTER)
time.sleep(1)
password.clear()
time.sleep(1)

# enter long password:
password.send_keys("abcdefghijklmnopqrstu")
time.sleep(1)

# submit the first test:
login.send_keys(Keys.ENTER)
time.sleep(1)
password.clear()
time.sleep(1)

# enter numeric password:
password.send_keys("123456")
time.sleep(1)

# submit the first test:
login.send_keys(Keys.ENTER)
time.sleep(1)
password.clear()
time.sleep(1)

# enter letters password:
password.send_keys("abcdefhijkl")
time.sleep(1)

# submit the first test:
login.send_keys(Keys.ENTER)
time.sleep(1)
password.clear()
time.sleep(1)

# enter correct password:
password.send_keys("eatCh0klate")
time.sleep(1)

# submit the first test:
login.send_keys(Keys.ENTER)
time.sleep(3)

# Close the browser
driver.quit()
