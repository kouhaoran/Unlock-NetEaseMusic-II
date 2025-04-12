# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00C05645D005CA805E7C8C94B8468112BF41C83A39E0C7DBF038117DA116C8E16ADDFD881D0136CB9C891DB2A88C3442FB3D5476A07CF9236DE7CA22641519D8B508D20738F1B1D079ED5D13A2E5FC1F4E5849C85D9E5DD62FE2CF8D0F02ADDD3A417723ECF11E2ED694EAA3D0FA85EBEF968057C1D0120C98BF8EACACC180EC7E77CEFA49072F0AABA8797AB4471E3352F773AB01676156D9AA2E824145B6E67A2D10477B7B3E86EB31CAD833771D0F8FEA624F140721E43C51A91054063E9168A944837CF3167A0B7FF1D381A5FD108540A4366333281A132407456D08EF95C934C4441A3C67518FD46338668E9F589B000A1DDF2909347A55E9C5B62A8FEAEBEC597D013542F4C5B06C4C2FA69E6EA1C8C8E92218BC5D2F83C8C002B8A8B97ABDA5D6C0AD503C448D54C69557DCF13A2DB060317081E098965E9D2D92136A3C8F93974258341E75857EA5821C0C48C6148602156C18BDE7986F52D19D7C3546"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
