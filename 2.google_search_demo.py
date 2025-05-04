import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument("--headless")  # Run in headless mode (no UI)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Setup WebDriver
driver = webdriver.Chrome(options=options)
# driver = webdriver.Firefox(options=options)
url_val = "https://www.google.com"
driver.get(url_val)
driver.find_element("name", "q").send_keys("Selenium Python")
# driver.find_element("name", "q").submit()

time.sleep(5)
