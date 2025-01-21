import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime

# Configuration
base_url = 'https://www.booking.com/index.es.html'
output_dir = './scraped_hotel_urls/'  # Directory to save the text files
hotels_webpage_class = 'a78ca197d0'
button_xpath = '//button[contains(@class, "bf0537ecb5")]'
next_month_button_xpath = '//button[contains(@class, "f073249358")]'


# Create output directory
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

def go_to_calendar_page(driver, current_date, target_date):
    """
    Navigates to the appropriate calendar pages to select the required dates.

    Args:
        driver: WebDriver instance.
        current_date (str): Current date in the format 'YYYY-MM-DD'.
        target_date (str): Target date in the format 'YYYY-MM-DD'.
    """
    # Convert strings to datetime objects
    current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    target_date_obj = datetime.strptime(target_date, "%Y-%m-%d")

    # Calculate the number of clicks needed
    month_diff = (target_date_obj.year - current_date_obj.year) * 12 + (target_date_obj.month - current_date_obj.month)

    # Navigate to the target month
    for _ in range(month_diff):
        next_month_button = driver.find_element(By.XPATH, next_month_button_xpath)
        next_month_button.click()
        time.sleep(1)

def scrape_hotels(city, start_date, end_date, number_of_cycles=5):
    """
    Scrape hotel URLs for a given city and date range.

    Args:
        city (str): City name to search for.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        number_of_cycles (int): Number of times to click 'Load More' button.

    Returns:
        int: Total number of hotels found.
    """
    print(f"Scraping {city} from {start_date} to {end_date}")

    driver.get(base_url)
    time.sleep(1)

    # Input city
    search_input = driver.find_element(By.ID, ':rh:')
    search_input.clear()
    search_input.send_keys(city)
    time.sleep(1)

    # Open calendar and select dates
    calendar_css = 'button.ebbedaf8ac:nth-child(2) > span:nth-child(1)'
    scroll_to_bottom(driver)  # Ensure calendar works on smaller screens
    driver.find_element('css selector', calendar_css).click()
    time.sleep(1)

    # Select start and end dates
    current_date = datetime.now().strftime("%Y-%m-%d")
    go_to_calendar_page(driver, current_date, start_date)
    date_start = driver.find_element(By.XPATH, f'//span[@data-date="{start_date}"]')
    date_start.click()
    time.sleep(1)

    go_to_calendar_page(driver, start_date, end_date)
    date_end = driver.find_element(By.XPATH, f'//span[@data-date="{end_date}"]')
    date_end.click()
    time.sleep(1)

    # Submit search
    search_button = driver.find_element(By.XPATH, '//*[@id="indexsearch"]/div[2]/div/form/div/div[4]/button')
    search_button.click()
    time.sleep(3)

    # Scroll and load more results
    cycle_count = 0
    while cycle_count < number_of_cycles:  # Adjust cycles for more results
        scroll_three_times(driver)
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            load_more_button.click()
            time.sleep(1)
        except Exception as e:
            print("No more 'Load More' button or error:", e)
            break
        cycle_count += 1
        print(f"Cycle {cycle_count} of {number_of_cycles} completed for {city} ({start_date} to {end_date})")

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
    print("=======================================")

    return len(hotel_urls)

# Scrape hotel URLs for Barcelona and Madrid
try:
    scrape_hotels("Barcelona", "2025-06-03", "2025-06-09", number_of_cycles=1) # 1 cycle is 100 hotels, +1 cycle = +25 hotels +-1
    scrape_hotels("Madrid", "2025-06-03", "2025-06-09", number_of_cycles=1)
    scrape_hotels("Barcelona", "2025-06-10", "2025-06-16", number_of_cycles=1)
    scrape_hotels("Madrid", "2025-06-10", "2025-06-16", number_of_cycles=1)
    print("=======================================")
    print("Scraping complete")
finally:
    driver.quit()
