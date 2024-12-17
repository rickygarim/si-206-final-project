from fetch_news import fetch_stock_news_monthly, clean_text
from sentiment_analysis import calculate_sentiment
from database_manager import save_news_to_db
from datetime import datetime

API_KEY = "CSM3Y8TKQYQXA09J"
STOCK_TICKERS = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "NFLX"]
start_date = "2024-09-01"
end_date = "2024-12-31"

print(f"Fetching data from {start_date} to {end_date}...")

for ticker in STOCK_TICKERS:
    news_data = fetch_stock_news_monthly(API_KEY, ticker, articles_per_month=1, start_date=start_date, end_date=end_date)
    save_news_to_db(news_data, ticker)

