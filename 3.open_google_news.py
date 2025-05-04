from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time


def get_google_news():
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        # Open Google News
        driver.get("https://news.google.com/")
        time.sleep(5)  # Allow time for page to load

        # Find news headlines
        headlines = driver.find_elements(By.XPATH, "//h3")

        # Extract and print news headlines
        news_list = [headline.text for headline in headlines if headline.text.strip() != ""]

        return news_list
    finally:
        driver.quit()


if __name__ == "__main__":
    news = get_google_news()
    for idx, headline in enumerate(news, start=1):
        print(f"{idx}. {headline}")
