#pip install selenium
# Selenium doesn't talk to browser directly, you need to use specific browser drivers
from selenium import webdriver
import time

driver = webdriver.Firefox()
# drive = webdriver.Chrome()
time.sleep(5)
# driver.get("https://www.saucedemo.com/")
#
# page_source = driver.page_source
# print(page_source)

# print(driver.title)
# driver.close()

