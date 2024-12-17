import sqlite3
import pandas as pd

class DataProcessingPipeline:
    def __init__(self, window_size, db_path):
        self.window_size = window_size
        self.db_path = db_path

    def _fetch_data(self):
        """Fetch stock data from the database."""
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT date, close_price FROM stock_data ORDER BY date"
            df = pd.read_sql(query, conn)  # Returns a DataFrame
        return df

    def _calculate_moving_average(self, df):
        """Calculate the moving average and add it as a column."""
        df['Date'] = pd.to_datetime(df['date'])
        df.sort_values('Date', inplace=True)  
        df[f'{self.window_size}-Day Moving Average'] = df['close_price'].rolling(window=self.window_size).mean()
        return df

    def process_data(self):
        """Fetch data, process it, and save back to the database."""
        # Fetch raw data
        raw_data = self._fetch_data()

        # Calculate Moving Average
        processed_df = self._calculate_moving_average(raw_data)

        # Save updated data back into the database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            for _, row in processed_df.iterrows():
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO stock_data (date, close_price, Moving_Average)
                        VALUES (?, ?, ?)
                    """, (
                        row['Date'].strftime('%Y-%m-%d'), 
                        row['close_price'], 
                        row[f'{self.window_size}-Day Moving Average']
                    ))
                except sqlite3.Error as e:
                    print(f"Error inserting data for {row['Date']}: {e}")

            conn.commit()

        print("Processed data saved to the database.")
