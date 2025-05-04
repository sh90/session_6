from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


def take_screenshot(url, file_name="screenshot.png"):
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Optional: Run in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        # Open the webpage
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load

        # Take a screenshot
        driver.save_screenshot(file_name)
        print(f"Screenshot saved as {file_name}")

    finally:
        driver.quit()


if __name__ == "__main__":
    take_screenshot("https://news.google.com/", "google_news.png")
