import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
load_dotenv()

# Set up Chrome options
# Create a new ChromeDriver instance
options = uc.ChromeOptions()
# options.add_argument("--headless=new")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
driver = uc.Chrome(options=options)

url = "https://www.doordash.com/reviews/store/126106/"

def signin():
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(os.environ['EMAIL'])
    time.sleep(5)
# Navigate to the website
driver.get(url)
time.sleep(5)
email = driver.find_element(By.XPATH, "//input[@type='email']")
if email:
    signin()
# reviews = driver.find_elements(By.XPATH, "/html/body/div/main/div/div/div/div/div/div/div/div[2]/div[2]")
# # print all the restaurant shop cards
# for review in reviews:
#     print(review)
#     print(review.text)

# # Close the driver and quit the browser
# driver.quit()

