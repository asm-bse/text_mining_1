
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = Chrome()

# Open Booking.com hotel page
url = 'https://www.booking.com/hotel/es/weflating-boutique-hostel.es.html?label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARnIAQzYAQHoAQH4AQKIAgGoAgO4AuqrsLwGwAIB0gIkNTNlNGJhZWQtODAzNS00OGVkLWJjODQtZDNlZWNjYjc4MmNh2AIF4AIB&aid=304142&ucfs=1&arphpl=1&dest_id=-372490&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0&hpos=14&hapos=14&sr_order=popularity&srpvid=127e937a3f790741&srepoch=1737233922&from=searchresults'

driver.get(url)

# Wait for the price element to appear
try:
    price_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "bui-price-display__value")]'))
    )
    hotel_price = price_element.text
    print(f"Hotel Price: {hotel_price}")
except:
    print("Price not found or page did not load properly.")

# Close the browser
driver.quit()
