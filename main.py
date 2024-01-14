# main.py
from utils import *
from data_processor import process_tournament_data
from bs4 import BeautifulSoup
from alive_progress import alive_bar
import json
import logging
import time

# Configuration
SPORTS_URL = "https://sports.bwin.com/en/sports/tennis-5/betting"

def retrieve_sports_betting_data(driver):
    logging.info("Accruing page location...")
    # Wait for the main content to load
    wait_for_element(driver, By.TAG_NAME, "ms-grid-header")
    # Find the ms-grid-header element
    grid_header = driver.find_element(By.TAG_NAME, "ms-grid-header")
    # Use ActionChains to move to the element and click
    actions = ActionChains(driver)
    actions.move_to_element(grid_header).click().perform()
    time.sleep(1)
    actions.send_keys(Keys.END).perform()
    time.sleep(1)
    actions.send_keys(Keys.HOME).perform()
    time.sleep(1)
    actions.send_keys(Keys.END).perform()
    time.sleep(3)
    actions.send_keys(Keys.PAGE_UP).perform()
    time.sleep(15) # wait for entire dom to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tennis_tournaments = soup.find_all("ms-event-group")

    extracted_data = []
    with alive_bar(len(tennis_tournaments), title='fetching tournament data', spinner='waves') as bar:
        for tournament in tennis_tournaments:
            tournament_data = process_tournament_data(tournament)
            extracted_data.append(tournament_data)
            bar()
    return extracted_data


def main():
    configure_logging()
    driver = initialize_webdriver()

    try:
        logging.info("Retrieving sports betting data...")
        driver.get(SPORTS_URL)

        extracted_data = retrieve_sports_betting_data(driver)

        logging.info("Exporting json file...")
        with open('tennis_data.json', 'w') as f:
            json.dump(extracted_data, f, indent=4)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
