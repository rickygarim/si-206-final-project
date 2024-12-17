import yfinance as yf
import sqlite3
import datetime

DB_NAME = "market_database.db"
TABLE_NAME = "tnx_data"
TICKER_SYMBOL = "^TNX"
START_DATE = "2023-01-01"
END_DATE = "2023-05-31"
BATCH_SIZE = 25
MAX_DAYS = 100
CLOSE_TIME = "16:00:00"

ticker = yf.Ticker(TICKER_SYMBOL)
hist = ticker.history(start=START_DATE, end=END_DATE)

data = []
for row in hist.itertuples():
    date_str = row.Index.strftime("%Y-%m-%d")
    close_value = row.Close
    data.append((date_str, close_value))

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute(f"""
    CREATE TABLE 
    IF NOT EXISTS {TABLE_NAME} (
        date TEXT PRIMARY KEY,
        time TEXT,
        value REAL
    )
    """
)

cursor.execute(f"""
    SELECT COUNT(*) 
    FROM {TABLE_NAME}
    """
)

current_count = cursor.fetchone()[0]

if current_count >= MAX_DAYS:
    print(f"Already have {MAX_DAYS} days of TNX data.")
    conn.close()
    exit()

if current_count > 0:
    cursor.execute(f"""
        SELECT date 
        FROM {TABLE_NAME} 
        ORDER BY date DESC 
        LIMIT 1
        """
    )
    last_date_str = cursor.fetchone()[0]
    
    last_idx = None
    for i, (d, v) in enumerate(data):
        if d == last_date_str:
            last_idx = i
            break

    start_index = last_idx + 1

else:
    start_index = 0

days_to_fetch = min(BATCH_SIZE, MAX_DAYS - current_count)
new_data = data[start_index:start_index+days_to_fetch]

if not new_data:
    print("No more TNX data to fetch.")
    conn.close()
    exit()

for d, v in new_data:
    cursor.execute(f"""
        INSERT OR 
        IGNORE INTO {TABLE_NAME} 
        (date, time, value) 
        VALUES (?, ?, ?)
        """,

        (d, CLOSE_TIME, v)
    )

conn.commit()
conn.close()

print(f"Inserted {len(new_data)} new days of TNX data. Total now: {current_count + len(new_data)} days.")
