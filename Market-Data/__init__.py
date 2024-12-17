import os
from api_pipeline import ApiPipeline
from database_pipeline import DatabasePipeline
from data_processing_pipeline import DataProcessingPipeline
from visualization_pipeline import VisualizationPipeline

class MarketDataStage:
    def __init__(self, chunks):
        market_data_api_key = "2Z5RECU4UTHZESBH"
        database_name = "stock_data.db"
        
        self.chunks = chunks 
        
        self.api = ApiPipeline(market_data_api_key, database_name)
        self.db = DatabasePipeline(database_name)
        self.processor = DataProcessingPipeline(4, database_name)
        self.visualizer = VisualizationPipeline(database_name)
    

    def run(self):
        # Call Api 
        for _ in range(chunks): 
            raw_data = self.api.fetch_data()

        # Save info to DB 
        self.db.save_data(raw_data)

        # Process Data
        processed_data = self.processor.process_data()
        
        # Visualize Data
        self.visualizer.visualize_data()

if __name__ == "__main__":
    pipeline = MarketDataStage()
    pipeline.run()
