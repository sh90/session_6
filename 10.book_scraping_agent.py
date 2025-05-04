# pip install langchain langchain-community selenium openai
#


import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
import data_info
# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = data_info.open_ai_key


# Define the tool using Selenium
@tool
def scrape_books(num_books: int = 10) -> str:
    """Scrape a given number of book titles and prices from books.toscrape.com."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("http://books.toscrape.com")

    books = driver.find_elements(By.CSS_SELECTOR, ".product_pod")[:num_books]
    results = []

    for book in books:
        title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
        price = book.find_element(By.CSS_SELECTOR, ".price_color").text
        results.append(f"{title} - {price}")

    driver.quit()
    return "\n".join(results)


# Initialize the language model (GPT-4o)
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Register the tool
tools = [scrape_books]

# Initialize the agent using OpenAI Functions (for structured input)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

# Ask your natural language question
query = "Get me the titles and prices of the first 8 books from books.toscrape.com"
response = agent.run(query)
print("\nScraped Results:\n" + response)
