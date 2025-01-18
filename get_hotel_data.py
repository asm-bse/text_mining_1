
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium import webdriver
import os
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

description_xpath = '//p[contains(@class, "b3efd73f69")]' #Not sure about sustainability of this xpath
description_class = 'a53cbfa6de b3efd73f69'

driver = Chrome()

with open('hotel_urls.txt') as f:
    for line in f:
        url = line.strip()
        driver.get(url)
        time.sleep(3)
        try:
            hotel_description = driver.find_element(By.XPATH, description_xpath).text
            #hotel_address = driver.find_element(By.XPATH, '//span[@id="showMap2"]').text
            #hotel_price = driver.find_element(By.XPATH, '//div[@class="bui-price-display__value prco-valign-middle-helper"]').text
            print('\n===============================\n')
            print(f"{hotel_description}")
            #print(f"{hotel_name}: {hotel_address}, {hotel_price}")
        except NoSuchElementException:
            print(f"Error: {url}")

time.sleep(99)
driver.quit()