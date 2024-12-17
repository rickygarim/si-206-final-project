import sqlite3

class DatabasePipeline:
    def _setup_database(self): 
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                close_price REAL NOT NULL, 
                Moving_Average REAL
            )
        ''')
        conn.commit()
        conn.close()
    
    def __init__(self, db_name):
        self.db_name = db_name
        self._setup_database()  # Call the correct setup method

    def save_data(self, data): 
        """Insert new stock data into the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        for record in data:
            try:
                cursor.execute('INSERT INTO price_data (date, close_price) VALUES (?, ?)', record)
            except sqlite3.IntegrityError:
                continue
        conn.commit()
        conn.close()
