import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import traceback
import json

def get_star(bg_postion):
    return {   
        "background-position: 0px 0px;": 1,
        "background-position: 0px -48px;": 2,
        "background-position: 0px -96px;": 3,
        "background-position: 0px -144px;": 4,
        "background-position: 0px -192px;": 5,
    }[bg_postion]

def handle_str(str):
    temp = str.split("\n")
    return {
        "reviewer": temp[1],
        "date": temp[2],
        "review": temp[4],
        "orders": temp[6:],
        "source": "grubhub"
    }

def gh_scraper(url: str, restaurant_id: int):
    # Set up Chrome options
    # Create a new ChromeDriver instance
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)

    # Navigate to the website
    driver.get(url)
    time.sleep(5)
    reviews = driver.find_elements(By.XPATH, "//div[@data-testid='restaurant-review-item']")
    data = []
    for review in reviews:
        try:
            revi = handle_str(review.text)
            revi['rating'] = get_star(review.find_element(By.XPATH, ".//div[@data-testid='stars-static']").get_attribute('style').strip())
            revi['restaurant_id'] = restaurant_id
            data.append(revi)
        except:
            traceback.print_exc()
            print(review)
    with open('data.json', 'w', errors = 'ignore') as f:
        json.dump(data, f)
    # Close the driver and quit the browser
    driver.quit()
    return data
