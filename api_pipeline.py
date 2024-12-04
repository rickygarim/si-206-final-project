class ApiPipeline:
    
    def __init__(self, market_data_key): 
        self.market_data_key = market_data_key
     
    def _get_stock_data(api_key): 
        # Get Stock Data API call, marked function as private
        pass 
    
    def fetch_data(self):
        marketData = get_stock_data() 
        
        return [marketData] 
