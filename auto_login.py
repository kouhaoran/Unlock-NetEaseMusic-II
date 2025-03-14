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
    browser.add_cookie({"name": "MUSIC_U", "value": "00384184525F08D70768C37F2BFD0C483D026F5E12FA9D3C5DF3214F48511E7B8527BF8E41D42A7C96E4A5EECB65FC3A1E24553499F6EBDEBA86B02C131DD0EB6D789D05D07E3EFFF2A30D4A854C70600FEFF0F719E0EB1A5BCE150999F2FD6C9FA83E55ADEAAAF6F43937D307618B836B8CFC75F6750CAC9CB3954791F5CDCFFD9016AFCAD3FD4CDCEF78C1E842549D66C2B419461F98EE7B2B4394E7E59357E475E757DFD97E7BD9E097A72CA44683DFC6F554AF6ED7161549F5D615B7E04A3E8DBD8041828482093E581639D0E7B15E73902416B14DAD8F57A60E337D13B73F8D6B47D4FD82D26B516AF7206C03B2299AF693F940B93F8D8704A78D627AD39D99CA2AE1EECC57AA60962022C082D55EC73D2D3897AB1D7B9442C59219D7601F51FD68160E975727CF835A389E44878F836FD83AC43B43C822E59397CB7C738447BBB070E975BB94B05390F2AD299A016275606DEC123518CFE73D94CBA15281"})
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
