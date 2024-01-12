from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from fractions import Fraction
import json
import time
import logging

options = Options()
options.headless = True

data = []

DRIVER_PATH = "C:\\Users\\Ben\\Documents\\Code\\Python\\outplayed_tech_test\\chromedriver_win32\\chromedriver.exe"
_path_to_chromedriver_linux = "C:\\Users\\Ben\\Documents\\Code\\Python\\outplayed_tech_test\\chromedriver_linux64\\chromedriver.exe"

logging.basicConfig(level=logging.INFO)


def bwin_scrape():
    extracted_data = []  # List to store extracted data

    # Instantiate the browser outside of 'with' statement
    driver = webdriver.Chrome()

    try:
        driver.get("https://sports.bwin.com/en/sports/tennis-5/betting")

        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "main-view"))
        )
        
        # Using By.XPATH in uppercase
        driver.find_element(
            By.XPATH, "/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar[2]/div/div/div/div/ms-main-column/div/ms-fixture-list/div/div/div/ms-fixture-list-header/ms-tab-bar/ms-scroll-adapter").click()
    
        # Additional wait for the main content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar[2]/div/div/div/div/ms-main-column/div/ms-fixture-list/div/div/div/ms-fixture-list-header/ms-tab-bar/ms-scroll-adapter"))
        )

        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        # Additional sleep to wait for potential JavaScript operations
        time.sleep(3)
        
        # Rest of your code...
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tennis_tournaments = soup.find_all("ms-event-group")

        timestamp = datetime.utcnow()

        for tournament in tennis_tournaments:
            tournament_name = tournament.find("div", class_="title").text

            tournament_data = {
                "tournament_name": tournament_name,
                "last_fetched": timestamp.strftime("%Y-%m-%d %H:%M"),
                "events": []
            }
            tennis_events = tournament.find_all("ms-event")
            for event in tennis_events:
                time.sleep(0.2)

                event_name = event.find("div", class_="participant").text
                date_time_element = event.find(
                    "ms-prematch-timer", class_="starting-time")

                if date_time_element:
                    date_time_str = date_time_element.text.strip()

                    try:
                        # Updated format for parsing time
                        date_time = datetime.strptime(date_time_str, "%m/%d/%y %I:%M %p")
                    except ValueError:
                        print(f"Could not parse date: {date_time_str}")
                        continue

                    date_time_string = date_time.strftime("%Y-%m-%d %H:%M")

                    if "live" not in event.get("class", []):
                        odds_elements = event.find_all("ms-font-resizer")

                        # Ensure there are at least two odds elements
                        if len(odds_elements) >= 2:
                            player_a_fractional = odds_elements[0].text.strip(
                            )
                            player_b_fractional = odds_elements[1].text.strip(
                            )

                            # Convert fractional odds to decimal format
                            player_a_odds_decimal = round(
                                float(Fraction(player_a_fractional)) + 1, 2)
                            player_b_odds_decimal = round(
                                float(Fraction(player_b_fractional)) + 1, 2)

                            # Store the extracted data
                            event_data = {
                                "event_name": event_name,
                                "start_time": date_time_string,
                                "outcomes": [
                                    {"outcome_name": "Player A",
                                        "odds": player_a_odds_decimal},
                                    {"outcome_name": "Player B",
                                        "odds": player_b_odds_decimal}
                                ]
                            }
                            tournament_data["events"].append(event_data)

            extracted_data.append(tournament_data)

    finally:
        # Manually close the browser to keep it open until the end
        driver.quit()

    # Now you can handle or return the extracted data outside the 'with' block
    return extracted_data


# Call the function to start scraping
extracted_data = bwin_scrape()

# You can now handle or print the extracted data as needed
with open('tennis_data.json', 'w') as f:
    json.dump(extracted_data, f)
