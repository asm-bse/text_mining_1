import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium import webdriver
import os
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

description_xpath = '//p[contains(@class, "b3efd73f69")]' #Not sure about sustainability of this xpath
description_class = 'a53cbfa6de b3efd73f69'
rating_xpath = '//div[contains(@id, "js--hp-gallery-scorecard")]'
rating_class = 'ac4a7896c7'
driver = Chrome()
directory = './scraped_hotel_urls/'
df = pd.DataFrame(columns=["URL", "Hotel", "Description", "City", "start_date", "end_date", "Rating", "Price"])

# Loop through the filenames
for filename in os.listdir(directory):
    # Create the full path
    file_path = os.path.join(directory, filename) #prevents us from hardcoding \ or /
    # Check if it's a file (not a directory)
    if os.path.isfile(file_path):
        print(f"Processing file: {filename}")
        city = filename.split('_')[0]  # The first part before the first underscore
        match = re.search(r'_(\d{4}-\d{2}-\d{2})_to_(\d{4}-\d{2}-\d{2})_', filename)
        if match:
            start_date = match.group(1)
            end_date = match.group(2)
        total_urls = 0
        processed_urls = 0
        print("====================================")
        with open(file_path) as f:
            lines = f.readlines()
            total_urls = len(lines)
            for line in lines:
                url = line.strip()
                processed_urls += 1
                driver.get(url)
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                hotel_rating = 999
                try:
                    price_element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "bui-price-display__value")]'))
                    )
                    hotel_price = price_element.text
                    #print(f"Hotel Price: {hotel_price}")
                except:
                    hotel_price = 9999999
                    print("Price not found or page did not load properly.")
                try:
                    hotel_description = driver.find_element(By.XPATH, description_xpath).text
                    hotel_name = driver.find_element(By.CLASS_NAME, 'pp-header__title').text
                    try:
                        rating_text = driver.find_element(By.XPATH, rating_xpath).text
                        rating_match = re.search(r'\d+(\.\d+)?', rating_text)
                        if rating_match:
                            hotel_rating = rating_match.group()
                    except Exception:
                        pass

                    df = pd.concat([df, pd.DataFrame([{"URL": url, "Hotel": hotel_name, "Description": hotel_description, "City": city,
                            "start_date": start_date, "end_date": end_date, "Rating": hotel_rating, "Price": hotel_price}])], ignore_index=True)

                except NoSuchElementException:
                    df = pd.concat([df, pd.DataFrame([{"URL": url, "Description": None}])], ignore_index=True)

                print(f"Processed {processed_urls}/{total_urls} URLs in {filename}")
                
                
time.sleep(1)
driver.quit()

df['Rating'] = df['Rating'].replace(999, 'NaN') #initially we put 999 as rating for hotels without rating, here we replace it with NaN
df.to_csv('scraped_hotel_data.csv', index=False)

print("Processing complete. Data saved to scraped_hotel_data.csv")
