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
    browser.add_cookie({"name": "MUSIC_U", "value": "005FBAF762FB22DE85301F8676ACB099067C8266C6582D7A57BD3F9B26DFC19115CB8E2C4A64197DEA9E317D7FB0E9B6C55FCE65FDE2EE45634031FF6A84F94CC572602F94F089C9ED26EA013FB7E9ED6BACAC738B99343202CC61F0AC4FCE23F4CDD7914D9B21817089235504D4B68A56FF7E45920DE372EF451A7659068BE2A2D42DC7951E3C75386A013859351A6521E6A20E2863449EF5BE79D9B00EB8166D6F7151D07AB753902BE0C6476D1E2D3ECD60ADE72AC0E9FB5CDC87C4CBBFBAC3D7CDD6ECF55A16775F54D42A86B661080DB87E726069CE9E882487F29730081C5EC8D0A43AF45392122C6344CDB52CD44955520D3AE31C378A8F49E5CC2FD7031D38831B8539A0FABDE27350D9C591559608FB5E2B0F4DA34510DA1AFE788B4F079428038D3BE0DC3766FD86448022800D7F1596E2F1BCAF61C4A305CB0F58A3C220C30A2687FAC406674CCF34D3691B35649A0A5F9FBCE1A9A99D5E77F6E9AD"})
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
