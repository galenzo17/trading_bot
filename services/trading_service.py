from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from config import API_KEY, SECRET_KEY, MAX_POSITION_SIZE
import logging
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

class TradingService:
    def __init__(self):
        self.client = TradingClient(API_KEY, SECRET_KEY, paper=True)
        self.logger = logging.getLogger(__name__)

        account_config = self.client.get_account_configurations()
        print(account_config)

    def open_position(self, symbol, notional):
        """Open a new position by placing a market order using notional amount."""
        try:
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                notional=notional,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )
            order = self.client.submit_order(order_data=market_order_data)
            self.logger.info(f"Opened position: Bought ${notional} worth of {symbol}")
            return order
        except Exception as e:
            self.logger.error(f"Error opening position for {symbol}: {e}")
            return None

    def close_position(self, symbol):
        """Close an existing position."""
        try:
            position = self.client.get_open_position(symbol_or_asset_id=symbol)
            qty = float(position.qty)
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.DAY
            )
            order = self.client.submit_order(order_data=market_order_data)
            self.logger.info(f"Closed position: Sold {qty} shares of {symbol}")
            return order
        except Exception as e:
            self.logger.error(f"Error closing position for {symbol}: {e}")
            return None


    def get_open_positions(self):
        """Retrieve all open positions."""
        try:
            positions = self.client.get_all_positions()
            return positions
        except Exception as e:
            self.logger.error(f"Error retrieving open positions: {e}")
            return []

    def calculate_order_quantity(self, symbol, price):
        """Calculate the number of shares to buy based on MAX_POSITION_SIZE."""
        try:
            qty = int(MAX_POSITION_SIZE / price)
            if qty > 0:
                return qty
            else:
                self.logger.warning(f"Calculated quantity is zero for {symbol} at price {price}")
                return None
        except Exception as e:
            self.logger.error(f"Error calculating order quantity for {symbol}: {e}")
            return None

    def get_account_status(self):
        """Get the account status and margin information."""
        try:
            account = self.client.get_account()
            return account
        except Exception as e:
            self.logger.error(f"Error fetching account information: {e}")
            return None
