# services/data_service.py

import alpaca_trade_api as tradeapi
from config import API_KEY, SECRET_KEY, BASE_URL
import logging

class DataService:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)
        self.logger = logging.getLogger(__name__)

    def get_current_price(self, symbol):
        """Get the current market price of a symbol."""
        try:
            barset = self.api.get_bars(symbol, tradeapi.TimeFrame.Minute, limit=1)
            if barset:
                price = barset[0].close  # Use the closing price of the latest bar
                return price
            else:
                self.logger.error(f"No bars returned for symbol: {symbol}")
                return None
        except Exception as e:
            self.logger.error(f"Error fetching current price for {symbol}: {e}")
            return None
