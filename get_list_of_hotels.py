import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
base_url = 'https://www.booking.com/index.es.html'
cities = ['Barcelona', 'Madrid']  #  cities
timeframes = [
    ('2025-01-25', '2025-02-10'),  # Event week
    ('2025-02-10', '2025-02-25')   # Non-event week
]
output_dir = './scraped_hotel_urls/'  # Directory to save the text files
hotels_webpage_class = 'a78ca197d0'
button_xpath = '//button[contains(@class, "bf0537ecb5")]'

# Create output directory
import os
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize WebDriver
driver = Chrome()

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def scroll_three_times(driver):
    for _ in range(3):
        scroll_to_bottom(driver)

# Start scraping
for city in cities:
    for start_date, end_date in timeframes:
        print(f"Scraping {city} from {start_date} to {end_date}")

        driver.get(base_url)
        time.sleep(3)

        # Input city
        search_input = driver.find_element(By.ID, ':rh:')
        search_input.clear()
        search_input.send_keys(city)
        time.sleep(1)

        # Open calendar and select dates
        calendar_css = 'button.ebbedaf8ac:nth-child(2) > span:nth-child(1)'
        driver.find_element('css selector', calendar_css).click()
        time.sleep(3)
        
        # Select start and end dates
        calendar_path = '//div[@id="calendar-searchboxdatepicker"]//table[@class="eb03f3f27f"]//tbody//td[@class="b80d5adb18"]//span[@class="cf06f772fa ef091eb985"]'
        dates = driver.find_elements('xpath', calendar_path)
        print(dates)
        for date in dates:
            if date.get_attribute("data-date") == start_date:
                date.click()
                time.sleep(1)
            elif date.get_attribute("data-date") == end_date:
                date.click()
                time.sleep(1)

        # Submit search
        search_button = driver.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/form/div/div[4]/button')
        search_button.click()
        time.sleep(5)

        # Scroll and load more results
        cycle_count = 0
        while cycle_count < 1:  # Adjust cycles for more results
            scroll_three_times(driver)
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
                load_more_button.click()
                time.sleep(3)
            except Exception as e:
                print("No more 'Load More' button or error:", e)
                break
            cycle_count += 1

        # Collect hotel URLs
        hotels = driver.find_elements(By.CLASS_NAME, hotels_webpage_class)
        hotel_urls = [hotel.get_attribute("href") for hotel in hotels]

        # Save results to a file
        filename = f"{output_dir}{city}_{start_date}_to_{end_date}_hotel_urls.txt"
        with open(filename, 'w') as f:
            for url in hotel_urls:
                f.write(f"{url}\n")

        print(f"Total hotels found for {city} ({start_date} to {end_date}): {len(hotel_urls)}")
        print(f"Results saved to {filename}")

driver.quit()
