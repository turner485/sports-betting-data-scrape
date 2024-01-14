# Sports Betting Data Retrieval Script

## Overview

This script is designed to retrieve sports betting data from a dynamic website using BeautifulSoup and Selenium. The script has been tested on both Windows10 and Ubuntu 22.04.3 (Linux) environments.

## Dependencies

- Python 3.x
- [pipenv](https://pipenv.pypa.io/en/latest/) for virtual environment management.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.
- [Selenium](https://www.selenium.dev/) for dynamic web page interaction.
- [Google Chrome](https://www.google.com/intl/en_uk/chrome/browser-tools/?_gl=1*b0ovt2*_up*MQ..*_ga*MTAzOTE2MzM1My4xNzA1MjU5MzM5*_ga_B7W0ZKZYDK*MTcwNTI1OTMzOC4xLjAuMTcwNTI1OTM1MC4wLjAuMA..&gclid=CjwKCAiAqY6tBhAtEiwAHeRopbrRW3QFlBXTHSozKXJINd8KFbsHH1JAMqOgTfOORcG6cvZ3PRJk1hoCWFAQAvD_BwE&gclsrc=aw.ds) for the script to run.

## Setup

1. Ensure you have Python 3.x installed on your system.

2. Install pipenv using the following command:

   ```
   cd outplayed_tech_test
   pip install pipenv
   pipenv --python path/to/python *
   pipenv install
   pipenv shell
   ```

*if you are not on the same python version that pipenv id requiring (3.9) you may encounter this message.

```Warning: your pipfile requires python_version 3.9, but you are using 3.x.x
```

this is fine, you should be able to continue with the set up commands, i have tested this numerous times.

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
- Due to time constraints, thorough unit tests and pytests have not been implemented.
