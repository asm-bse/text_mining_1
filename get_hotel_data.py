
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
df = pd.DataFrame(columns=["URL", "Hotel", "Description", "City", "Date", "Rating"])
# Loop through the filenames
for filename in os.listdir(directory):
    # Create the full path
    file_path = os.path.join(directory, filename) #prevents us from hardcoding \ or /
    # Check if it's a file (not a directory)
    if os.path.isfile(file_path):
        print(f"Processing file: {filename}")
        city = filename.split('_')[0]  # The first part before the first underscore
        match = re.search(r'(\d{4}-\d{2}-\d{2}_to_\d{4}-\d{2}-\d{2})', filename)
        date = match.group(1)
    with open(file_path) as f:
        for line in f:
            url = line.strip()
            driver.get(url)
            time.sleep(3)
            hotel_rating = 999
            try:
                print(date)
                hotel_description = driver.find_element(By.XPATH, description_xpath).text
                hotel_name = driver.find_element(By.CLASS_NAME, 'pp-header__title').text
                try:
                    rating_text = driver.find_element(By.XPATH, rating_xpath).text
                    #print(f"Rating text: {rating_text}") uncomment for debugging or parcing more feedback features
                    rating_match = re.search(r'\d+(\.\d+)?', rating_text)
                    if rating_match:
                        hotel_rating = rating_match.group()
                        #print(f"Hotel rating: {hotel_rating}")
                    else:
                        print("Rating not found")
                except Exception as e:
                    print(f"Error: {e}")
                #hotel_rating = driver.find_element(By.XPATH, rating_class).text
                #hotel_address = driver.find_element(By.XPATH, '//span[@id="showMap2"]').text
                #hotel_price = driver.find_element(By.XPATH, '//div[@class="bui-price-display__value prco-valign-middle-helper"]').text
                print('\n===============================\n')
                print(f"Hotel name: {hotel_name}\n")
                print(f"{hotel_description}\n")
                print(f"Hotel rating: {hotel_rating}\n")

                df = pd.concat([df, pd.DataFrame([{"URL": url, "Hotel":hotel_name, "Description": hotel_description, "City": city,
                        "Date": date, "Rating": hotel_rating}])], ignore_index=True)
                #print(f"{hotel_name}: {hotel_address}, {hotel_price}")
            except NoSuchElementException:
                print(f"Error: {url}")
                df = pd.concat([df, pd.DataFrame([{"URL": url, "Description": None}])], ignore_index=True)
                
time.sleep(3)
driver.quit()

df['Rating'] = df['Rating'].replace(999, 'NaN') #initially we put 999 as rating for hotels without rating, here we replace it with NaN
df.to_csv('scraped_hotel_data.csv', index=False)

print(df.head())
