# services/data_service.py

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
from config import API_KEY, SECRET_KEY
import logging

class DataService:
    def __init__(self):
        self.client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
        self.logger = logging.getLogger(__name__)

    def get_current_price(self, symbol):
        """Get the current market price of a symbol."""
        try:
            request_params = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            latest_quote = self.client.get_stock_latest_quote(request_params)
            price = latest_quote[symbol].ask_price
            return price
        except Exception as e:
            self.logger.error(f"Error fetching current price for {symbol}: {e}")
            return None
