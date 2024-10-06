from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta
from typing import List
from selenium.common.exceptions import WebDriverException
from prefect import task
import uuid
import hashlib
import os

def create_uuid_from_string(val):
    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return str(uuid.UUID(hex=hex_string))[:8]


def is_date_in_current_week(date: datetime) -> bool:
    """Checks if a given date is in the current week."""
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    return start_of_week <= date <= end_of_week

def setup_driver() -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    try:
        SELENIUM_URL = os.getenv("SELENIUM_URL", "http://selenium:4444/wd/hub")
        return webdriver.Remote(SELENIUM_URL, options=chrome_options)
    except WebDriverException:
        print("Unable to connect to driver")

def scroll_to_bottom(driver: WebDriver, max_scroll_height: int) -> None:
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if max_scroll_height and new_height >= max_scroll_height:
            print(f"Reached maximum scroll height of {max_scroll_height} px")
            break
        if new_height == last_height:
            break
        last_height = new_height
        
def scrape_article_cards(driver: WebDriver) -> List[dict]:
    articles = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup.find_all('div', class_='timeline-description')
    
    for card in cards:
        title = card.find('h2').text.strip()
        date = card.find('span', class_='timestamp').text.strip()
        summary = card.find('div', class_='timeline-body-text-wrapper').text.strip()
        tags = card.find('div', class_='tag-list theme').text.replace('Theme tags: ', '').strip()
        uuid = create_uuid_from_string(title)

        date_object = datetime.strptime(date, "%B %d, %Y")

        if is_date_in_current_week(date_object) and 'Hack' in tags:

            formatted_date_obj = date_object.strftime("%Y-%m-%d")
            
            articles.append({
                'id': uuid,
                'title': title,
                'date': formatted_date_obj,
                'summary': summary,
                'tags': tags
            })


    
    return articles


@task(name="Fetching Hack Data", log_prints=True, retries=3)
def fetch_hack_data(file_name: str, data_path: str) -> None:
    driver = setup_driver()
    driver.get('https://www.web3isgoinggreat.com/')
    max_scroll_height = 1

    try:
        # Wait for the first card to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "timeline-description"))
        )
        
        # Scroll to load all content
        scroll_to_bottom(driver, max_scroll_height)
        
        # Scrape the loaded content
        articles = scrape_article_cards(driver)

        df = pd.json_normalize(articles)

        df.to_csv(data_path + file_name, index=False)
    
        
    finally:
        driver.quit()