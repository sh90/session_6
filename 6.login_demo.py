import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def selenium_automation():
    # Set up WebDriver (Make sure you have the correct WebDriver installed)
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")

    # Fill the login form
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    time.sleep(5)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    time.sleep(5)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(5)  # Wait for page to load

    # Extract product names
    products = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    for product in products:
        print("Product:", product.text)

    # Close the browser
    #driver.quit()

if __name__ == "__main__":
    selenium_automation()
