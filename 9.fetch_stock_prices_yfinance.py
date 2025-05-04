# pip install tabulate
# pip install yfinance
import yfinance as yf
import pandas as pd
import openai
import data_info

openai.api_key = data_info.open_ai_key
def get_stock_data(ticker, start_date, end_date):
    """
    Retrieves stock market data from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL" for Apple).
        start_date (str): The start date for the data (YYYY-MM-DD).
        end_date (str): The end date for the data (YYYY-MM-DD).

    Returns:
        pandas.DataFrame: A DataFrame containing the stock data, or None if an error occurs.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        return data

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def display_stock_data(data):
  """
  Displays the stock data nicely, or prints a message if there's no data.
  """
  if data is not None and not data.empty:
        print(data) #pandas dataframes print nicely
  elif data is None:
        print("No stock data retrieved.")
  else:
    print("No data in the specified date range.")

  # Perform time series calculation on the data
  response = openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": "Can you analyse this time series data and calculate 20 moving average" + data.to_markdown(index=False)}],
      temperature=0.1
  )

# Example usage:
ticker_symbol = "MSFT"  # Example: Microsoft
start_date = "2025-02-01"
end_date = "2025-03-31"

stock_data = get_stock_data(ticker_symbol, start_date, end_date)
display_stock_data(stock_data)

#Example of multiple tickers.
tickers = ["AAPL"]
all_data = yf.download(tickers, start=start_date, end=end_date)
display_stock_data(all_data)

#Example with specific data fields
data_specific = yf.download(tickers, start=start_date, end=end_date)['Close'] #Gets only adjusted closing prices
display_stock_data(data_specific)
