# utils.py
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import logging

WAIT_TIME = 20

def configure_logging():
    selenium_logger = logging.getLogger('selenium')
    selenium_logger.setLevel(logging.ERROR)
    logging.basicConfig(level=logging.INFO)

def initialize_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--enable-javascript")
    chrome_options.add_argument("log-level=3")
    chrome_options.add_experimental_option(
        "prefs", {'profile.managed_default_content_settings.images': 2}
    )

    return webdriver.Chrome(options=chrome_options)

def wait_for_element(driver, by, value):
    return WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((by, value))
    )
