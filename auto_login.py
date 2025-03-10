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
    browser.add_cookie({"name": "MUSIC_U", "value": "003D0878FB499F8BA3218EABAAAE6AECEE20BAAC81D8C72CBD6BAF0F1EDADD2FB3C523FDA4C9F67E800BB9BB80CF834B7A1864A37CB70FC1FBE8D4272F609683405E7EA33D9D3B2B8A9951AAF99F77E273AE98355695632E83E38C43C578B5B3D7E03607ABE2E032DDC89931B1D509ADA65EBFF43271A072CE0D975C733A1DD61B0DA8DB241553CAEA06C20B80B91D02BCBC8D0D2E644D646CAE3E853B03C6C5E3B7105542FD42644BAB7A4A64D1333BE3879FC9153293BBBBDA764C112931ADB575495672C51325F0D89DF4E60E840E6C8A8C50F94EC0003BD3940CF9F9C16852213889C53F3425C5A6E4C09A491C09D7D2AED78F1F37E2665D4104B536F892C14F7FC09A7CB678A795A54BC368EA0B151764D6BBE9E171F909A4FA69CFB099394CE9305F55369A874C3F147336201C6EEC44F7A6AB5EB58582D4096470143ABFD64BBE00CEF72E343DC4D2F87245F952295EC69595E7AB51B980581533121C3F"})
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
