import os
from dotenv import load_dotenv

from api_pipeline import ApiPipeline
from database_pipeline import DatabasePipeline
from data_processing_pipeline import DataProcessingPipeline
from visualization_pipeline import VisualizationPipeline

class DataPipeline:
    def __init__(self):
        
        load_dotenv()
        market_data_api_key = os.getenv('MARKET_DATA_KEY')
        
        self.api = APIPipeline(market_data_api_key)
        self.db = DatabasePipeline()
        self.processor = DataProcessingPipeline()
        self.visualizer = VisualizationPipeline()

    def run(self):
        # Call Api 
        raw_data = self.api.fetch_data()

        # Save info to DB 
        self.db.initialize_database()
        self.db.save_data(raw_data)

        # Process Data
        processed_data = self.processor.process_data(raw_data)
        
        # Visualize Data
        self.visualizer.visualize_data(processed_data)

if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run()
