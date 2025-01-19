
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import re
'''
            try:
                buttons = driver.find_elements(By.XPATH, '//button[@data-testid="date-display-field-start"]')
                if len(buttons) > 1:
                    check_in_button = buttons[1]  # Index 1 for the second button
                    check_in_button.click()
                else:
                    print("Second button not found")
                # Use the data-testid attribute for a precise and robust selector
                time.sleep(3)  # Allow time for the calendar to open
            except NoSuchElementException:
                print("Calendar button not found.")

'''
# Input string
filename = "Barcelona_2025-10-10_to_2025-10-25_hotel_urls.txt"

# Regular expression to match the date format 'YYYY-MM-DD_to_YYYY-MM-DD'
match = re.search(r'(\d{4}-\d{2}-\d{2}_to_\d{4}-\d{2}-\d{2})', filename)

if match:
    # Extract the date range
    date_range = match.group(1)
    print(date_range)
else:
    print("No date range found in the string.")


driver = Chrome()

# Open Booking.com hotel page
url = 'https://www.booking.com/hotel/es/45-times-barcelona-hotel.es.html?aid=304142&label=gen173nr-1FCAEoggI46AdIClgEaEaIAQGYAQq4ARnIAQzYAQHoAQH4AQKIAgGoAgO4AryHtbwGwAIB0gIkOTFkYmJhZjAtMGJlMC00ZDRkLWEyNmItMjhjOGVhMmM3ODBh2AIF4AIB&sid=b36672d4d17b0f7730ff53b950e235d6&all_sr_blocks=255329702_245098339_2_2_0_313494&checkin=2025-01-25&checkout=2025-02-10&dest_id=-372490&dest_type=city&dist=0&group_adults=2&group_children=0&hapos=2&highlighted_blocks=255329702_245098339_2_2_0_313494&hpos=2&matching_block_id=255329702_245098339_2_2_0_313494&nad_cpc=1.09&nad_id=6ab9aa5b-e33b-4252-a814-93864480902d_0&nad_track=eyJhdWN0aW9uRXBvY2giOjE3MzczMTExNzY5MzcsInJhbmsiOjEsImtvZGRpVHJhY2tpbmdJbmZvIjoiT1h6UDBTS0NTM0FJeFB6RGlCS1VSUlpEbzVQTml1K3N3QS9IaVNzbHVSWXpWMjBqMlVHN3RFVkx2MmZzbDI3U29qd1g3TUw0STVEajg4N1FmZFBBWGh2NXZadkszbjYrVWc2bm5oMFNERGhmQWR0NEh2SVRDQjFTUzluSXJQRkQ1NzFxV2E4RXF5dWF4MUZYTGpvWWcya3hCekZNODdFSjN5ZUxGV2VWSDd4cnFoK1ErMkpQanRxYnZsdDBlb0ZoZ1EzT0NYRWVxQnNib25WNkJUYys2UjYzdDNLcWs0d1RicUp3b2xnSHRMVCszeHQxVWM1OExrdWlvcjBJRElQWTlLWERsdTVRbmoreGtNTThVMEpMbkxhdXhlWkZlS0wzWG5kMGE1S3RxQmpUREw3bG1qUHVsTG1SeVo5YkNyTWZtelA1MXBOSTJxeWNDRE9KZXdpc2VNQTdJL1FVakFjQ1FMRTBrWXRtejZydzJvYnpVcGNESy9IaDFUVDV4T1RUakpNVERHRDl1VGpqZ2w3ZXdmNUpDekM5SVRPVlNHYUFqNG9iY3Y0WWM0SDA2VWRldTlmRXlDcWxjVFlLQkdIdVZyNFZsMk1XcUtuOXNxS1Vyd00rNDlzU2plLzFQYkI4RVpJMUE3cTlHc29waEFndThtNi9Sc3ZJU0pyZUx6N0VwNy8rcDVJazBXKzhEbnZra2FmTHJaTVVYZU5qZE1WNjlIcWZjakJoQ2ZmcjBPNVBmajdtNU9ReFl4OFArbklvcjMvY2FuL0J3UGlaTXBYUXNEa1JSOHhDeTVtOWNhcG9XSXZsdzVtc2J4T0M1MUpSRFlkbWlGWHd5aTNHeWJjZUlUYTB2L3k0MTZGRkpsbXpmd2FDTy9Wa3U1U3FtNVVsb1pEbnEvNlAwRFRpbVdaVlNxdVRRdXM1ZHdYUXZFOTRIZ3djMHE3U2UrMVNTdFBZSllQeTk1TDJnaDZ2bUJYWUl3bnFKLzVSN0Vjcm5CQnhyU1hMeEZDZkNBbTJjVThncTZQK1NiNFhHZ09mQ0JDalZsMGk5VHVwdUxISUlBUlZpMk5QOUZpSkwyNjJBTWJlQTFSZ0R1RUNtQjNNYlhMZWg3QllSQzI0ckdMcGpMQTFoME1NMmlheVRVOUt4ZzI4YW1oQ3RidENOVnMvR3R4K09PLzFVcnZuQ2JHMzJFOWNiSmNieXhzYU16QXVUTnlFZFIzanpseFA5MWVzYndYRXpUZ0pkZHNwN2MwUkJTbm5NdnFBUXNCT0dzV1hML1hrdE1Ba0Jjb05vems2SXdMbmd6OU1raTZoSWRZRXZPWkRUM0ZVaTJyZ01BNW5MdWExSVVGYUdOUFZWeEtRRGN5WW5PQitldlhMNkpMS2VSUFBvMDlFenJqb1BjSVdGNHpoZHpxMUN5MGhuMFhzWUpINDNVMS9tM0dxM1pJc0ZOenhvSTFCNTI5VmsrYzk4SmJjWHA3WXBONUdDNjhVZG9GaUJaSklUUGNJUzEwZmdsZHdjVk1zbHdDbXBhcUJsMmszSXpZYkpuSVVNQXQ3TXQwckxqS2lPNDNMcFcrdlZ0YzNRRFF2YUtpT0lIY3h3YTViTkxaMXJ1WFpqOWtRS0xzQk11VWxJOFZ5cExNSWoxRGczb1loMGI0Rm42REpEMTBSend0bEhUWFhPL1lOTnRmZWRzR3lDYXF4NC96N0ttai92cjRnbURsZlNpVFcvbm9UN1NtQ2VjTTNmSWQvNkVoenV1VUdNa1VHUCtyVk9PZTFPbnk5REtoSEtkZkRSV0hTWmEyRHZaZVBvK1FDYzhtbUYzSHh5ckthRmgxZWNQVE5yZDVtVnE5NCtTMEFNR2trcEkxWUVNUXptNHBldjVPSC9nbllvSnppQTc0SFhWN2VreEVXNVVxcFIvUGJINWkyT1ZNemxJbUk3d0wyMkhCNlZ6amt4eEVSWlpDaytyUmZiRUs4REVaWWRPamJVNlJ2MGhrV25qSnBQYnphcEhUcUhlVkowUWZMU3M1M0FKR1R6Ky83OGZDZFBZS0ZxdGJRN0dqNXc2aURqQUhYeHh2bUZLU24xTlpGVm5DWFhuUHBkWEJ1a2JrTjA5YWtQMThoTlZqMTdGRnZrK1RUcFQxZEJQVUJmTjlKNE9hb1E5elgvVTk5T0dmMWU1bm1LVTJuQUNrOExqeW1sRVhUeWNLaHl3UDFtWWhrMG81Sks3ZUVsV0F3Y1dnVEFZdVVNRFdBQ2h0MmZneW5UUW5EaXFVVFMrTkRXdjRabEpzUDFkV1Y4SE5sdWJZRVh5Yit2MTdwbjd0R28va0ZOblpUUGtlNDhNeE1wQlpzcXZNVDNRMWx5TDJBS0VPMjhYNGlOWGY5Vm0rZzFxQzIyTzI1NWZXMzNoRHpEV1VmbkRwbDZoSy9vRjBPa1paYUY2c2JQYjlXdzN1M0xjWjJkQjlJN3YxL2Q4WTVzZGcrVDVNQkVIamNUVkJyT2xxZ2pqN1krU082VEExbEZsMkk0UjZaalFQQ0FCMFVyWnlBL3h1Mjh2V0FDQzY2UlJFOGtlNWZqU1o4QWl1dFlmeVloaUZ1NC82V3UwcWU3MDNmZGxkbUgrZmFyV2VrTjlLdzl1czVOZ0c0NkFtQVljcWd4QlkvZ0pyVHN0bm5QMFhKOGF4VVRXL284VkZBTHpYN1U4L2hLMGFMblFqd1dVYXVrZ0d6Y25wb0FiZm9kREtsNU5CMkw2dDZZQXNWT2NwNkpZd2FhUHlpM3BQNllJQVRIQzM3TWNVRmpUUWcwUGdpVWwvMHdTazBRNG93R2NZUXpvTUFhdHJNMVRVelpPNGhBLzJ4T0ptcDBrS0JVY1dCQXViZW14YUh3bVRmQWp1S0hBZVRLN09KVWpQYk1GTTZVZ1JkaS9XNWtwNUdmWCtMNm1SNE1yUFRLNWtuNi9WdWhBVTZ4bUlsWTZtZEVyUW1pZDNsaHpQOVZ0SG1kbVhTeGJXQmlWSTJyK3NkcEp6TjhvMVdKejA1WUpJVEliK0EvS3BHUDhmcUFNMXljWlh4c3B1elJQdUFYbVRWdHJtdnVxbXl5ektsc2JiY2xveVA5aFRRdGppRnVXalhsNm1jQ0hpbE1Jc2xpZmVOZ2M2eHROSTZwTWJxcWZqdklSeGFtQit1cThZMTFmRjR0WnVYSEQ3enU5SUlTSzNMNUtVUlV3Y2c2Rnd1N0p4bElrV1RXRHhDc1NhUTdnOCtqMkJWdlN0QXFvN1NEWGVrZmg5dDZqZmJvRk9kR3AzZXdZOUp3bmhkUjNmVm9LZjdJeWk0c0Ric2NtUElrZ1FsU3h5YjBHempSdHB6a3VlTHlqS080NW9VMldNUy9FK29Vb041QU5MSkYrTlo1Y3J1Vm1CZFJSRllzWnVJNnQxdXU4UGM3UTNUT0FOeXhkOExQSCtRd09EWWxBZng4RWUrV0l6VlJ0Vjhib0VjVlozMWdQdG0rNDVpelE9PSJ9&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&sr_pri_blocks=255329702_245098339_2_2_0_313494_475745&srepoch=1737311191&srpvid=158581a4e0500708&type=total&ucfs=1&'

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
