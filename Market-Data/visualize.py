import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def visualize_sentiment_subplots(db_name="Market-Data/market_database.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ticker, timestamp, sentiment_score FROM stock_news
        ORDER BY timestamp
    """)
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No data available to plot.")
        return

    tickers = sorted(set(row[0] for row in rows))
    num_tickers = len(tickers)
    rows_subplot = (num_tickers + 3) // 4

    fig, axes = plt.subplots(rows_subplot, 4, figsize=(14, 2.5 * rows_subplot), sharex=True, sharey=True)
    axes = axes.flatten()

    for idx, ticker in enumerate(tickers):
        ticker_data = [row for row in rows if row[0] == ticker]
        timestamps = [datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S.%fZ") for row in ticker_data]
        sentiment_scores = [row[2] for row in ticker_data]

        ax = axes[idx]
        ax.plot(timestamps, sentiment_scores, marker="o", linestyle="-", label=ticker, color="tab:blue")
        ax.set_title(f"{ticker}", fontsize=8, pad=10)
        ax.tick_params(axis="x", rotation=45, labelsize=7)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator())

    for i in range(len(tickers), len(axes)):
        fig.delaxes(axes[i])

    plt.subplots_adjust(hspace=0.5, wspace=0.4)
    fig.suptitle("Sentiment Scores Over Time by Company", fontsize=12, y=0.92)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    visualize_sentiment_subplots(save_path="sentiment_graph.png")
