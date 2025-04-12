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
    browser.add_cookie({"name": "MUSIC_U", "value": "001D60E1865E1EE357A1AA1E120345ED0E50BFEE2F5F0BDBEFE805AB336CC18A624C930CAE0925A49329B9AB5E960138DB8C70AAFEA8858839BE22A5090A42369304663ADEBB6E1F1AD14E0F5D1E717AA24F6FB959B32435A840A27B43577F40F46945CF68ECE94D84FEF89C0E7F798E1133187FD601466702A07FAD9DACC239AB25503D9CD71C7134E423645F10BF5EEFBD15C109860FE7EBD0C5D1E505613B04DA3801BE17F91536229164EB124FE9C312CEDE7B7B64CD326F801F2BCE9633FF3B22FB7C667801D29CBF787699A5CB995984C8E270534DE06721C13DB680F00DE484CB1EDDACAD8B1E2DBC11C37E0C385019401924B827BE133E2992A084BD55BC3BFD2C0D069E3ED7A65F51B3BE6E7D28E2AA5961D758B1ADAAD88B284312ECD0720CE47F7098FF1C419F8E1092D425E4CEC41CDB1BA4B667642D5624B02AFD2E46040DFCBBD4ABA8B2007FC972357408D3D489D13EA8B1E97DB61E6E374CD2"})
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
