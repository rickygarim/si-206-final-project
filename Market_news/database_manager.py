import sqlite3
from fetch_news import clean_text
from sentiment_analysis import calculate_sentiment

def save_news_to_db(news_data, stock_ticker, db_name="Market-Data/market_database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create table with timestamp column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_news (
            id INTEGER PRIMARY KEY,
            ticker TEXT,
            title TEXT,
            description TEXT,
            timestamp TEXT,
            sentiment_score REAL,
            UNIQUE(title)  -- Prevent duplicate entries
        )
    """)

    for news in news_data:
        title = clean_text(news.get("title", ""))
        description = clean_text(news.get("description", ""))
        timestamp = news.get("published_at", "")
        if not timestamp:
            continue  # Skip if timestamp is missing
        
        sentiment_score = calculate_sentiment(title)

        try:
            cursor.execute("""
                INSERT OR IGNORE INTO stock_news (ticker, title, description, timestamp, sentiment_score)
                VALUES (?, ?, ?, ?, ?)
            """, (stock_ticker, title, description, timestamp, sentiment_score))
        except sqlite3.IntegrityError:
            print(f"Duplicate entry skipped: {title[:30]}...")

    conn.commit()
    conn.close()
