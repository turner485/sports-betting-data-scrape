# data_processor.py
from datetime import datetime, timedelta
from fractions import Fraction
import logging
import time
import re

def convert_start_time(start_time_str):
    if start_time_str:
        # Extract the minutes using regular expression
        minutes_match = re.search(r'(\d+)\s*min', start_time_str)
        minutes = int(minutes_match.group(1)) if minutes_match else 0

        now = datetime.utcnow()

        if 'Today' in start_time_str or 'Starting' in start_time_str:
            if minutes > 0:
                start_time = now + timedelta(minutes=minutes)
            else:
                try:
                    # Try parsing 'Starting' or 'Today' format
                    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
                        hours=now.hour, minutes=now.minute
                    )
                except ValueError:
                    logging.error(f"Error parsing time: {start_time_str}")
                    return None

            return start_time.strftime('%Y-%m-%d %H:%M')
        elif 'Tomorrow' in start_time_str:
            time_str = start_time_str.split(
            )[-2] + " " + start_time_str.split()[-1]
            return (now + timedelta(days=1)).strftime('%Y-%m-%d ') + datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')
        elif '/' in start_time_str:
            start_date_time_obj = datetime.strptime(
                start_time_str, '%m/%d/%y %I:%M %p')
            return start_date_time_obj.strftime('%Y-%m-%d %H:%M')

    logging.info("Date not found or match is past/in play - No odds to fetch")
    return None

def process_event_data(event, participant_elements, date_time_element):
    if participant_elements and len(participant_elements) == 2:
        start_date_time = convert_start_time(
            date_time_element.text.strip()) if date_time_element else None

        if start_date_time:
            player_a_name = participant_elements[0].text.strip()
            player_b_name = participant_elements[1].text.strip()

            odds_elements = event.find_all("ms-font-resizer")

            if odds_elements and len(odds_elements) >= 2:
                player_a_fractional = odds_elements[0].text.strip()
                player_b_fractional = odds_elements[1].text.strip()

                player_a_odds_decimal = round(
                    float(Fraction(player_a_fractional)) + 1, 2)
                player_b_odds_decimal = round(
                    float(Fraction(player_b_fractional)) + 1, 2)

                event_data = {
                    "event_name": f"{player_a_name} v {player_b_name}",
                    "start_time": start_date_time,
                    "outcomes": [
                        {"outcome_name": player_a_name,
                            "odds": player_a_odds_decimal},
                        {"outcome_name": player_b_name,
                            "odds": player_b_odds_decimal},
                    ],
                }
                return event_data
    else:
        logging.info(
            "Participant elements not found or incomplete. Skipping event.")
        return None

def process_tournament_data(tournament):
    tournament_name = tournament.find("div", class_="title").text
    tournament_data = {
        "tournament_name": tournament_name,
        "last_fetched": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        "events": []
    }

    tennis_events = tournament.find_all("ms-event")

    for event in tennis_events:
        time.sleep(0.3)
        participant_elements = event.find_all("div", class_="participant")
        date_time_element = event.find(
            "ms-prematch-timer", class_="starting-time")

        event_data = process_event_data(
            event, participant_elements, date_time_element)

        if event_data:
            tournament_data["events"].append(event_data)

    return tournament_data
