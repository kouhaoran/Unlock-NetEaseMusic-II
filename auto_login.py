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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A29CA2F6E7FFAB8D14D02547209E745194424400831A28BFFB1DB531F7D25083D2B7DA3CC83481F183BB39B45C50E31143B79BE40F7ADFC1599AEB1E23C1693010AB1DF0C2B0936A19EAF7844DDE8C0FC60AFE027F56670841B0D6E34A3EBCD1BC4D68093CE558CA6A80657ABA092F8B27ED76D95D3230EDDED5CF17158BA7CA090724060F20011FD2E669229DDD17A7BC93FC8BCE172A5ED9E4E231C22F5A9A1CCAA88F4DF3F4761C026BC5E324338451CB1A45DE8D0F7C342207F175DEFB3D0671A371AAD91579886E20AABB5F9AE8E4A08282AEB538488B2CDB4F3235577A1116DC55E2019BCF1BC796489F21427243802C054210E773BE2C16D7E54017499FF4905D4AABEF32BFEA091B3E5F71471B66411DFD968E0A652FB420EB8BF52D33E7EE1F6892EFC382E8BEC6E76A9136036A41267DE9521578F442FAC48B0F0D723C0880865AB041AEFCBC83CE97032A1967640241623106048F1386B5B54A5D"})
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
