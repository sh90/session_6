import time
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import data_info
options = Options()
# options.add_argument("--headless")  # Run in headless mode (no UI)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Set up OpenAI API key
openai.api_key = data_info.open_ai_key

# Function to extract HTML from a webpage using Selenium
def get_html_with_selenium(url):
    driver = webdriver.Chrome(options=options)
    # driver.get("https://www.google.com")
    driver.get(url)

    # Wait for page to load
    time.sleep(5)  # Can increase if page takes longer to load

    # Get page source after it has fully loaded
    html_content = driver.page_source
    reviews_div = driver.find_element(By.XPATH, '//*[@id="reviewsMedley"]')

    # Alternatively, if the div has a unique class name, you can use:
    # reviews_div = driver.find_element(By.CLASS_NAME, 'reviewsMedley')

    # Get the content of the div (for example, extracting the text content)
    reviews_content = reviews_div.text
    # driver.quit()

    return reviews_content


# Function to process HTML content with GPT-4
def process_html_with_gpt(html_content):
    prompt = f"""
    The following is a block of raw HTML. Please extract and summarize the reviews for a product from the HTML:

    Please extract:
    - Reviewer names
    - Review text
    
      {html_content}
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    return response.choices[0].message.content.strip()


# Main function to scrape and process data from a website
def extract_reviews_from_website(url):
    # Get raw HTML content using Selenium
    html_content = get_html_with_selenium(url)
    # Process the HTML with GPT-4 to extract meaningful reviews
    review_summary = process_html_with_gpt(html_content)
    return review_summary


# Example usage
if __name__ == "__main__":
    # Test with a sample Yelp or other review page (replace with real URL)
    # parse_url = "https://www.yelp.com/biz/dave-and-busters-daly-city-11"
    parse_url = "https://www.amazon.in/Tecno-Segments-Processor-Fluency-Battery/dp/B0DGMG1DN2/ref=sr_1_1_sspa?_encoding=UTF8&content-id=amzn1.sym.83d39114-85e6-4972-a6b9-854fbd1dbde2&dib=eyJ2IjoiMSJ9.a3_271uwgmGA9sdvpAMmIMYfXpw0ayxO-_hviXESpmvs_scdVvRFAKll3MVxmgB63tkqH43kHFQFiPofyak5-GH7TMRNVs1h0k4QLdllNLKawOhFWUuwWqRXGiaqdDm-K_GrFhK0bdGzDEXWhcJIRZ3tzH3f8IRWwvryOnaXTuqzpUSVNRzHYpg3ctsNZuHJQudrnuVsNJSaHTbd0gidz_gWmXXXcBpJGoa5nnq4AhiqAB_jZCDMhqlLnu8g2yZG5TEt7v-Hak_70W3t3XZGQ7aox8qQkMYBA1oj-1IiGEk.yDR3cqXSnsbsizq-I-jCwTmiFaDSoVx0G_9f4E7sPmY&dib_tag=se&pd_rd_r=8efe7010-f4a1-4ce3-9264-b8ebe8f723f4&pd_rd_w=0WTEz&pd_rd_wg=Mgq91&qid=1746267294&refinements=p_36%3A-1030000&rnid=1318502031&s=electronics&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGZfYnJvd3Nl&psc=1"
    url = parse_url

    # Extract and process reviews
    extracted_review_summary = extract_reviews_from_website(url)

    # Display the result
    print("Extracted Review Summary:")
    print(extracted_review_summary)
