# Sports Betting Data Retrieval Script

## Overview

This script is designed to retrieve sports betting data from a dynamic website using BeautifulSoup and Selenium. The script has been tested on both Windows and Ubuntu (Linux) environments.

## Dependencies

- Python 3.x
- [pipenv](https://pipenv.pypa.io/en/latest/) for virtual environment management
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Selenium](https://www.selenium.dev/) for dynamic web page interaction

## Setup

1. Ensure you have Python 3.x installed on your system.

2. Install pipenv using the following command:

   ```
   cd outplayed_tech_test
   pip install pipenv
   pipenv install
   pipenv shell
   ```

## Running the script
The script retrieves sports betting data from a dynamic website. It uses Selenium to gain control and scroll the site, allowing the DOM to load. This is necessary because the site's content is dynamic and may not be fully loaded when initially accessed.

To run the script, execute the following command:

`python main.py`

## Notes
- The script utilizes Selenium for dynamic interactions, ensuring that the necessary content is loaded before data retrieval.
- pipenv is requires 3.9 as specified.
- for any matches in play the data will **NOT** be fetched.
- For testing purposes, the script has been verified on both Windows and Ubuntu (Linux) environments.
- The virtual environment is managed using pipenv for a clean and isolated development environment.
- additional setup instructions may be required based on your operating system and environment.
- due to time constraints i didn't have time to do my regular unittests & pytests. 