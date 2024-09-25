# services/trading_service.py

import alpaca_trade_api as tradeapi
from config import API_KEY, SECRET_KEY, BASE_URL, MAX_POSITION_SIZE, TAKE_PROFIT_PERCENTAGE, STOP_LOSS_PERCENTAGE
import logging

class TradingService:
    def __init__(self):
        self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)
        self.logger = logging.getLogger(__name__)

    def open_position(self, symbol, qty):
        """Open a new position by placing a market order."""
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='day'
            )
            self.logger.info(f"Opened position: Bought {qty} shares of {symbol}")
            return order
        except Exception as e:
            self.logger.error(f"Error opening position for {symbol}: {e}")
            return None

    def close_position(self, symbol):
        """Close an existing position."""
        try:
            position = self.api.get_position(symbol)
            qty = abs(float(position.qty))
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='day'
            )
            self.logger.info(f"Closed position: Sold {qty} shares of {symbol}")
            return order
        except tradeapi.rest.APIError as e:
            self.logger.error(f"No position to close for {symbol}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error closing position for {symbol}: {e}")
            return None

    def get_open_positions(self):
        """Retrieve all open positions."""
        try:
            positions = self.api.list_positions()
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

    def place_bracket_order(self, symbol, qty, take_profit_price, stop_loss_price):
        """Place a bracket order with take-profit and stop-loss."""
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='day',
                order_class='bracket',
                take_profit={'limit_price': take_profit_price},
                stop_loss={'stop_price': stop_loss_price}
            )
            self.logger.info(f"Placed bracket order for {symbol}: qty={qty}, take_profit={take_profit_price}, stop_loss={stop_loss_price}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing bracket order for {symbol}: {e}")
            return None
