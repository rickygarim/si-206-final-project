import sqlite3

class DatabasePipeline:
    def __init__(self, name):
        self.name = name 

    def initialize_database(self):
        pass  

    def save_data(self, data):
        pass