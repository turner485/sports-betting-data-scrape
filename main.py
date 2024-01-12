# selenium imports
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# rest of imports
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from fractions import Fraction
import json, logging, time

#selenium logging
selenium_logger = logging.getLogger('selenium')
selenium_logger.setLevel(logging.ERROR)

#custom logging
logging.basicConfig(level=logging.INFO)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--enable-javascript")
chrome_options.add_argument("log-level=3")
chrome_options.add_experimental_option(
    "prefs", {'profile.managed_default_content_settings.images': 2}
)

# Global Variables
now = datetime.utcnow()
# init list
extracted_data = []  

def sports_betting_data_retrieval():
    
    logging.info("Retrieving sports betting data...")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://sports.bwin.com/en/sports/tennis-5/betting")
    logging.info("Accruing page location...")
    ### wait block ###
    time.sleep(2)
    # Wait for the main content to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "ms-grid-header"))
    ).click()
    time.sleep(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.END).perform()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "footer"))
    )
    actions.send_keys(Keys.HOME).perform()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "ms-grid-header"))
    ).click
    actions.send_keys(Keys.END).perform()
    time.sleep(14) #time taken to load entire DOM

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tennis_tournaments = soup.find_all("ms-event-group")

    for tournament in tennis_tournaments:
        tournament_name = tournament.find("div", class_="title").text
        tournament_data = {
            "tournament_name": tournament_name,
            "last_fetched": now.strftime("%Y-%m-%d %H:%M"),
            "events": []
        }

        # Find the tennis events within the current tournament
        tennis_events = tournament.find_all("ms-event")

        for event in tennis_events:
            time.sleep(0.5)
            # get player data
            participant_elements = event.find_all("div", class_="participant")
            # get time/date data
            date_time_element = event.find(
                "ms-prematch-timer", class_="starting-time")

            
          
            
            if date_time_element:
                start_date_time_str = date_time_element.text.strip()
                # declare time string   
                time_str = start_date_time_str.split()[-2] + " " + start_date_time_str.split()[-1]
                # Covert Today time/date
                if 'Today' in start_date_time_str:
                    start_date_time = now.strftime('%Y-%m-%d ') + \
                        datetime.strptime(
                            time_str, '%I:%M %p').strftime('%H:%M')
                # Covert Tomorrow time/date
                elif 'Tomorrow' in start_date_time_str:
                    start_date_time = (now + timedelta(days=1)).strftime(
                        '%Y-%m-%d ') + datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')
                # Rest of Time/Date conversions
                elif '/' in start_date_time_str:
                    start_date_time_obj = datetime.strptime(start_date_time_str, '%m/%d/%y %I:%M %p')
                    time_str = start_date_time_obj.strftime('%Y-%m-%d %H:%M')
                    start_date_time = time_str
                    logging.info(start_date_time)
                else:
                    logging.info("Date not found")
                    continue
            else:
                logging.info("Match Past or in play - No odds to fetch")
                continue

            # Check if the participant element was found
            if len(participant_elements) == 2:
                player_a_name = participant_elements[0].text.strip()
                player_b_name = participant_elements[1].text.strip()
                print("Match:", player_a_name, " v ", player_b_name)
            else:
                logging.info("Participant element not found.")
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

# Call the function and logging.info the result
extracted_data = sports_betting_data_retrieval()
logging.info("Exporting json file...")
with open('tennis_data.json', 'w') as f:
    json.dump(extracted_data, f)
