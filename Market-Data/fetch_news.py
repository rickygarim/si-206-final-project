import requests
from bs4 import BeautifulSoup
import calendar
from datetime import datetime, timedelta
import sqlite3

def fetch_stock_news_monthly(api_key, stock_ticker, articles_per_month=1, start_date=None, end_date=None, db_name="market_database.db"):
    url = "https://api.marketaux.com/v1/news/all"
    all_news = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_news (
            id INTEGER PRIMARY KEY,
            ticker TEXT,
            title TEXT,
            description TEXT,
            timestamp TEXT,
            sentiment_score REAL,
            UNIQUE(ticker, title, timestamp)  -- Prevent duplicate entries
        )
    """)
    conn.commit()

    while current_date <= datetime.strptime(end_date, "%Y-%m-%d"):
        month_start = current_date.replace(day=1)
        last_day = calendar.monthrange(month_start.year, month_start.month)[1]
        month_end = current_date.replace(day=last_day)

        params = {
            "api_token": api_key,
            "symbols": stock_ticker,
            "language": "en",
            "limit": articles_per_month * 3,
            "published_after": month_start.strftime("%Y-%m-%dT00:00:00"),
            "published_before": month_end.strftime("%Y-%m-%dT23:59:59"),
            "group_similar": "true",
            "must_have_entities": "true"
        }

        print(f"Fetching up to {articles_per_month} new articles for {stock_ticker} in {month_start.strftime('%B %Y')}...")
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json().get("data", [])
            new_articles = []
            for news in data:
                title = clean_text(news.get("title", ""))
                description = clean_text(news.get("description", ""))
                timestamp = news.get("published_at", "")

                # Check for duplicates in the database
                cursor.execute("SELECT 1 FROM stock_news WHERE ticker=? AND title=? AND timestamp=?", 
                               (stock_ticker, title, timestamp))
                if not cursor.fetchone():
                    new_articles.append(news)

                if len(new_articles) >= articles_per_month:
                    break

            all_news.extend(new_articles)
            print(f"Fetched {len(new_articles)} new articles for {stock_ticker} in {month_start.strftime('%B %Y')}.")
        else:
            print(f"Error fetching for {stock_ticker}: {response.status_code}, {response.text}")

        # Move to the next month
        current_date = (month_start + timedelta(days=32)).replace(day=1)

    conn.close()
    return all_news

# Step 2: Clean Text Using BeautifulSoup
def clean_text(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()