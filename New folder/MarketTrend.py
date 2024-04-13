import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_market_trend(company_symbol):
    # Construct the URL of the market information page on Yahoo Finance
    url = f'https://finance.yahoo.com/quote/{company_symbol}'

    # Send a GET request to the website and retrieve the HTML content
    response = requests.get(url)

    # Check if the request is successful
    if response.status_code == 200:
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the HTML element containing the stock price information
        price_element = soup.find('span', {'data-reactid': '50'})

        # Check if the price value exists
        if price_element:
            price = price_element.text.strip()
            return price
        else:
            return None
    else:
        return None

# Define a list of company symbols
company_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']

# Create an empty DataFrame to store the data
data = {'Company': [], 'Stock Price': []}
df = pd.DataFrame(data)

# Retrieve stock prices for each company symbol and store them in the DataFrame
for symbol in company_symbols:
    price = get_market_trend(symbol)
    if price is not None:
        df = df.append({'Company': symbol, 'Stock Price': price}, ignore_index=True)

# Print the DataFrame
print(df)
