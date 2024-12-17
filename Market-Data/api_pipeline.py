import requests
import sqlite3
from datetime import datetime, timedelta

class ApiPipeline:
    
    def __init__(self, market_data_key, db_name): 
        self.market_data_key = market_data_key
        self.db_name = db_name

    
    def _get_latest_date(self):
        """Fetch the latest stored date from the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(date) FROM stock_data')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result[0] else None

    def _get_stock_data(self): 
        """Fetch stock data from the API."""
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&outputsize=full&symbol=SPY&apikey={self.market_data_key}'
        response = requests.get(url)
        return response.json().get("Time Series (Daily)", {})
    
    def fetch_data(self): 
        latest_date = self._get_latest_date()
        
        # Increment start_date by 1 day if data exists, otherwise start from Jan 1, 2023
        if latest_date:
            start_date = datetime.strptime(latest_date, "%Y-%m-%d") + timedelta(days=1)
        else:
            start_date = datetime(2023, 1, 1)
        
        stock_data = self._get_stock_data()
        
        # Sort the data by ascending date (oldest first)
        sorted_data = sorted(stock_data.items(), key=lambda x: x[0])
        new_data = []
        
        for date, details in sorted_data:
            # Include only dates on or after the start_date
            if datetime.strptime(date, "%Y-%m-%d") < start_date:
                continue
            
            # Collect the next 25 records
            close_price = float(details["4. close"])
            new_data.append((date, close_price))
            if len(new_data) >= 25:  # Limit to 25 days
                break
        
        return new_data
