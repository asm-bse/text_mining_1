import os
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
base_url = 'https://www.booking.com/index.es.html'
cities = ['Barcelona', 'Madrid']  # Cities to scrape
timeframes = [
    ('2025-10-10', '2025-10-25'),  # Event week
    ('2025-11-01', '2025-11-15')   # Non-event week
]
output_dir = './scraped_hotel_urls/'  # Directory to save the text files
hotels_webpage_class = 'a78ca197d0'
button_xpath = '//button[contains(@class, "bf0537ecb5")]'

# Create output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize WebDriver
driver = Chrome()
wait = WebDriverWait(driver, 10)

def scroll_to_bottom(driver):
    """Scroll to the bottom of the page."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

def scroll_three_times(driver):
    """Scroll the page three times."""
    for _ in range(3):
        scroll_to_bottom(driver)

def select_date(date_value):
    """Selects a date in the calendar by its 'data-date' attribute."""
    try:
        date_xpath = f'//td[@data-date="{date_value}"]'
        date_element = wait.until(
            EC.element_to_be_clickable((By.XPATH, date_xpath))
        )
        date_element.click()
        print(f"Selected date: {date_value}")
    except Exception as e:
        print(f"Could not select date {date_value}: {e}")

# Start scraping
for city in cities:
    for start_date, end_date in timeframes:
        print(f"Scraping {city} from {start_date} to {end_date}")

        # Open base URL
        driver.get(base_url)
        time.sleep(3)

        # Input city
        try:
            search_input = wait.until(EC.presence_of_element_located((By.ID, ':rh:')))
            search_input.clear()
            search_input.send_keys(city)
        except Exception as e:
            print(f"Error setting city {city}: {e}")
            continue

        # Open calendar
        try:
            calendar_button_xpath = '//button[@data-testid="date-display-field-start"]'
            calendar_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, calendar_button_xpath))
            )
            calendar_button.click()
        except Exception as e:
            print(f"Error opening calendar: {e}")
            continue

        # Select start and end dates
        select_date(start_date)
        select_date(end_date)

        # Submit search
        try:
            search_button_xpath = '//*[@id="indexsearch"]/div[2]/div/form/div/div[4]/button'
            search_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, search_button_xpath))
            )
            search_button.click()
        except Exception as e:
            print(f"Error clicking search button: {e}")
            continue

        time.sleep(5)  # Wait for the search results to load

        # Scroll and load more results
        cycle_count = 0
        while cycle_count < 1:  # Adjust cycles for more results
            scroll_three_times(driver)
            try:
                load_more_button = wait.until(
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
        try:
            hotels = driver.find_elements(By.CLASS_NAME, hotels_webpage_class)
            hotel_urls = [hotel.get_attribute("href") for hotel in hotels]
        except Exception as e:
            print(f"Error collecting hotel URLs: {e}")
            hotel_urls = []

        # Save results to a file
        filename = os.path.join(output_dir, f"{city}_{start_date}_to_{end_date}_hotel_urls.txt")
        with open(filename, 'w') as f:
            for url in hotel_urls:
                f.write(f"{url}\n")

        print(f"Total hotels found for {city} ({start_date} to {end_date}): {len(hotel_urls)}")
        print(f"Results saved to {filename}")

# Close the driver
driver.quit()
