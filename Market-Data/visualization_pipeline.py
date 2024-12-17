import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

class VisualizationPipeline:
    def __init__(self, db_path):
        self.db_path = db_path

    def _fetch_data_from_db(self):
        """Fetch stock data from the database."""
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT date, close_price, Moving_Average FROM price_data ORDER BY date"
            df = pd.read_sql(query, conn)
        return df

    def visualize_data(self):
        """Visualize stock prices and moving averages."""
        # Load data
        df = self._fetch_data_from_db()

        # Plot Data
        df['Date'] = pd.to_datetime(df['date'])
        plt.figure(figsize=(10, 6))
        plt.plot(df['Date'], df['close_price'], label='Stock Price', color='blue', marker='o', linestyle='-', markersize=5)
        plt.plot(df['Date'], df['Moving_Average'], label='Moving Average', color='red', linestyle='--')
        plt.title('Stock Price and Moving Average')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.legend(loc='upper left')
        plt.grid(True)
        plt.tight_layout()

        save_path = os.path.join(os.getcwd(), 'visuals', 'stock_moving_average_plot.png')
        plt.savefig(save_path)

        print(f"Plot saved to {save_path}")
        plt.close()
