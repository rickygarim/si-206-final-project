import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import string

# Step 1: Fetch Stock News API Data
def fetch_stock_news(api_key, stock_ticker, limit=100, from_date=None, to_date=None):
    url = f"https://api.marketaux.com/v1/news/all"
    params = {
        "api_token": api_key,
        "symbols": stock_ticker,
        "language": "en",
        "limit": limit,
        "from": from_date,  # Start date for fetching news
        "to": to_date       # End date for fetching news
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

# Step 2: Clean Text Using BeautifulSoup
def clean_text(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# Step 3: Save News Data to Database
def save_news_to_db(news_data, stock_ticker, db_name="stocks.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_news (
            id INTEGER PRIMARY KEY,
            ticker TEXT,
            title TEXT,
            description TEXT,
            timestamp TEXT,
            sentiment_score REAL
        )
    """)
    
    for news in news_data:
        title = clean_text(news.get("title", ""))
        description = clean_text(news.get("description", ""))
        timestamp = news.get("published_at", "")
        sentiment_score = calculate_sentiment(title)  # Calculate sentiment score
        cursor.execute("""
            INSERT INTO stock_news (ticker, title, description, timestamp, sentiment_score)
            VALUES (?, ?, ?, ?, ?)
        """, (stock_ticker, title, description, timestamp, sentiment_score))
    
    conn.commit()
    conn.close()

# Step 4: Basic Sentiment Analysis
def calculate_sentiment(text):
    """
    Calculate sentiment based on weighted scores for weak, moderate, and strong positive/negative words.
    """
    # Predefined word dictionaries
    weak_positive_words = {"good", "up", "gain", "improved", "bullish"}
    moderate_positive_words = {"great", "success", "rally", "growth", "strong"}
    strong_positive_words = {"beat", "win", "profit"}

    weak_negative_words = {"bad", "down", "miss", "weak"}
    moderate_negative_words = {"decline", "fall", "drop", "sell", "plunge"}
    strong_negative_words = {"loss", "failure", "bearish"}

    # Preprocess text
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    words = text.split()

    # Sentiment categories
    weak_positive_count = sum(1 for word in words if word in weak_positive_words)
    moderate_positive_count = sum(1 for word in words if word in moderate_positive_words)
    strong_positive_count = sum(1 for word in words if word in strong_positive_words)

    weak_negative_count = sum(1 for word in words if word in weak_negative_words)
    moderate_negative_count = sum(1 for word in words if word in moderate_negative_words)
    strong_negative_count = sum(1 for word in words if word in strong_negative_words)

    # Raw sentiment score calculation
    raw_sentiment_score = (
        weak_positive_count * 1 + moderate_positive_count * 2 + strong_positive_count * 3 +
        weak_negative_count * -1 + moderate_negative_count * -2 + strong_negative_count * -3
    )

    # Adjusted sentiment score
    denominator = (
        (weak_positive_count + weak_negative_count) * 1 +
        (moderate_positive_count + moderate_negative_count) * 2 +
        (strong_positive_count + strong_negative_count) * 3 +
        100  # Bayesian extra value
    )

    if denominator == 0:
        return 0  # Avoid division by zero

    adjusted_sentiment_score = raw_sentiment_score / denominator

    print(f"Text: {text} | Adjusted Sentiment Score: {adjusted_sentiment_score}")
    return adjusted_sentiment_score


# Step 5: Visualize Sentiment Over Time
def visualize_sentiment(db_name="stocks.db", from_date=None, to_date=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ticker, timestamp, sentiment_score FROM stock_news
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY timestamp
    """, (from_date + "T00:00:00Z", to_date + "T23:59:59Z"))
    rows = cursor.fetchall()
    conn.close()

    tickers = set(row[0] for row in rows)
    for ticker in tickers:
        ticker_data = [row for row in rows if row[0] == ticker]

        # Parse timestamps for the decade range
        timestamps = [
            datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S.%fZ") for row in ticker_data
        ]
        sentiment_scores = [row[2] for row in ticker_data]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, sentiment_scores, marker="o", label=ticker)
        plt.title(f"Sentiment Scores Over Time for {ticker} (Last Decade)")
        plt.xlabel("Timestamp")
        plt.ylabel("Sentiment Score")
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        plt.gca().xaxis.set_major_locator(mdates.YearLocator())
        plt.legend()
        plt.tight_layout()
        plt.show()

# Main Execution
if __name__ == "__main__":
    # API Key and Stock Tickers
    API_KEY = "hy0Fr7NXBy3XT6YnIZB8jVq02Z1JTTicjsQjMVUA"
    STOCK_TICKERS = ["AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "NFLX", "NVDA", "META", "ADBE", "INTC"]
    # Calculate date range (past decade)
    today = datetime.utcnow()
    decade_ago = today - timedelta(days=365 * 10)  # Approximate 10 years

    # Format dates as strings (e.g., "YYYY-MM-DD")
    today_str = today.strftime("%Y-%m-%d")
    decade_ago_str = decade_ago.strftime("%Y-%m-%d")

    print(f"Fetching data from {decade_ago_str} to {today_str}")

    # Fetch and save news data for each stock ticker
    for ticker in STOCK_TICKERS:
        print(f"Fetching news for {ticker} from {decade_ago_str} to {today_str}")
        news_data = fetch_stock_news(API_KEY, ticker, from_date=decade_ago_str, to_date=today_str)
        save_news_to_db(news_data, ticker)

    # Visualize sentiment over the past decade
    visualize_sentiment(db_name="stocks.db", from_date=decade_ago_str, to_date=today_str)
