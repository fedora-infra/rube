import logging
selenium_logger = logging.getLogger("selenium.webdriver")
selenium_logger.setLevel(logging.INFO)

from selenium import webdriver

driver = None

def get_driver():
    global driver
    if not driver:
        driver = webdriver.Firefox()
    return driver

def tearDown():
    if driver:
        driver.close()
