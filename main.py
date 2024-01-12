from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from fractions import Fraction
import json
import time
import logging

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_experimental_option(
    "prefs", {'profile.managed_default_content_settings.images': 2}
)

def sports_betting_data_retrieval():
    extracted_data = []  # List to store extracted data

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://sports.bwin.com/en/sports/tennis-5/betting")

    # Wait for the main content to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "ms-grid-header"))
    ).click()
    print("Accruing page location...")
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "footer"))
    )
    actions.send_keys(Keys.HOME).perform()
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, "ms-grid-header"))
    ).click
    actions.send_keys(Keys.END).perform()
    time.sleep(14) #time taken to load entire DOM

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tennis_tournaments = soup.find_all("ms-event-group")

    for tournament in tennis_tournaments:
        tournament_name = tournament.find("div", class_="title").text
        timestamp = datetime.utcnow()
        tournament_data = {
            "tournament_name": tournament_name,
            "last_fetched": timestamp.strftime("%Y-%m-%d %H:%M"),
            "events": []
        }

        # Find the tennis events within the current tournament
        tennis_events = tournament.find_all("ms-event")

        for event in tennis_events:
            time.sleep(0.5)

            participant_elements = event.find_all("div", class_="participant")
            date_time_element = event.find(
                "ms-prematch-timer", class_="starting-time")

            if date_time_element:
                start_date_time_str = date_time_element.text.strip()

                if 'Today' in start_date_time_str:
                    # Extract time only
                    time_str = start_date_time_str.split(
                    )[-2] + " " + start_date_time_str.split()[-1]
                    start_date_time = datetime.now().strftime('%Y-%m-%d ') + \
                        datetime.strptime(
                            time_str, '%I:%M %p').strftime('%H:%M')

                elif 'Tomorrow' in start_date_time_str:
                    # Extract time only
                    time_str = start_date_time_str.split(
                    )[-2] + " " + start_date_time_str.split()[-1]
                    start_date_time = (datetime.now() + timedelta(days=1)).strftime(
                        '%Y-%m-%d ') + datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')

                else:
                    print(f"Unsupported date format: {start_date_time_str}")
                    continue
            else:
                print("Match Past or in play - No odds to fetch")
                continue

            # Check if the participant element was found
            if len(participant_elements) == 2:
                player_a_name = participant_elements[0].text.strip()
                player_b_name = participant_elements[1].text.strip()
                print("Match:", player_a_name, " v ", player_b_name)
            else:
                print("Participant element not found.")
                continue

            odds_elements = event.find_all("ms-font-resizer")
            if odds_elements and len(odds_elements) >= 2:
                player_a_fractional = odds_elements[0].text.strip()
                player_b_fractional = odds_elements[1].text.strip()

                player_a_odds_decimal = round(
                    float(Fraction(player_a_fractional)) + 1, 2)
                player_b_odds_decimal = round(
                    float(Fraction(player_b_fractional)) + 1, 2)

                print("Odds:", player_a_odds_decimal, player_b_odds_decimal)

                event_data = {
                    "event_name": player_a_name + " v " + player_b_name,
                    "start_time": start_date_time,
                    "outcomes": [
                        {"outcome_name": player_a_name,
                            "odds": player_a_odds_decimal},
                        {"outcome_name": player_b_name,
                            "odds": player_b_odds_decimal},
                    ],
                }
                tournament_data["events"].append(event_data)

        # Append the tournament_data to the extracted_data list
        extracted_data.append(tournament_data)

    driver.quit()

    return extracted_data

# Call the function and print the result
extracted_data = sports_betting_data_retrieval()
print("Exporting json file...")
with open('tennis_data.json', 'w') as f:
    json.dump(extracted_data, f)
