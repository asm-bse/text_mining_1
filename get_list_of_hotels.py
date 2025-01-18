import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium import webdriver
import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://www.booking.com/index.es.html'
city_path = '//*[@id=":rh:"]'
#date_path = '//*[@id="indexsearch"]/div[2]/div/form/div/div[2]'
search_button_path='//*[@id="indexsearch"]/div[2]/div/form/div/div[4]/button'
calendar_path='//div[@id="calendar-searchboxdatepicker"]//table[@class="eb03f3f27f"]//tbody//td[@class="b80d5adb18"]//span[@class="cf06f772fa ef091eb985"]'

place = 'Barcelona'
start_date = '2025-10-10'
end_date = '2025-11-11'
number_of_cycles = 3 #each cycle is 3 scrolls and 1 click on "Load more" button, +25 hotels per cycle +-

css='button.ebbedaf8ac:nth-child(2) > span:nth-child(1)'



driver = Chrome()
driver.get(url)
time.sleep(3)
#driver.find_element(by=By.XPATH,value=date_path).click()
driver.find_element('css selector',css).click()
time.sleep(3)

dates = driver.find_elements('xpath',calendar_path)
#for date in dates:
    #print(date.get_attribute("data-date"))


date_day_before_last = dates[-2].get_attribute("data-date")
date_last_day = dates[-1].get_attribute("data-date")

day_before_last = dates[-2].click()
time.sleep(1)
last_day = dates[-1].click()
print(f'Last day: {date_last_day}')
print(f'Day before last: {date_day_before_last}')

time.sleep(1)

search1 = driver.find_element(by='xpath',value=city_path)
search1.send_keys(place)

time.sleep(1)

search1 = driver.find_element(by='xpath',value=search_button_path).click() #we can emulate ENTER button by using send_keys('\n') instead of click()

current_url = driver.current_url
print(f"Original URL: {current_url}")

# Replace dates in URL
modified_url = current_url.replace(date_day_before_last, start_date)
modified_url = modified_url.replace(date_last_day, end_date)
print(f"Modified URL: {modified_url}")
time.sleep(3)
# Navigate to new URL
driver.get(modified_url)
time.sleep(3)

hotels_webpage_class = 'a78ca197d0'
button_load_more_class = 'a83ed08757 c21c56c305 bf0537ecb5 f671049264 af7297d90d c0e0affd09'
button_xpath = '//button[contains(@class, "bf0537ecb5")]' #Not sure about sustainability of this xpath

def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def scroll_three_times():
    for _ in range(3):
        scroll_to_bottom()
        print("Scrolled down")

cycle_count = 0
while cycle_count < number_of_cycles:
    # 3 scrolls
    scroll_three_times()
    time.sleep(2)
    # Click button
    try:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
        load_more_button.click()
        print("Button clicked successfully")
    except Exception as e:
        print(f"Error: {e}")
    cycle_count += 1


# Collect URLs
hotels = driver.find_elements(By.CLASS_NAME, hotels_webpage_class)
hotel_urls = []
for hotel in hotels:
    hotel_urls.append(hotel.get_attribute("href"))

with open('hotel_urls.txt', 'w') as f:
    for url in hotel_urls:
        f.write(f"{url}\n")

print(f"Total hotels found: {len(hotel_urls)}")
driver.quit()
