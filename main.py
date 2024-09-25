# main.py

import time
import threading
from services.trading_service import TradingService
from services.data_service import DataService
from utils.helpers import setup_logging
from config import STOCKS, TAKE_PROFIT_PERCENTAGE, STOP_LOSS_PERCENTAGE
import logging

def idle_mode(trading_service, data_service):
    """Function to run in idle mode, continuously checking prices."""
    logger = logging.getLogger(__name__)
    logger.info("Entering idle mode...")
    while True:
        for symbol in STOCKS:
            price = data_service.get_current_price(symbol)
            if price:
                # Implement your trading logic here
                logger.info(f"Current price of {symbol}: {price}")
                # Example: Check if we should open a position
                qty = trading_service.calculate_order_quantity(symbol, price)
                if qty:
                    # For simplicity, we open a position if we don't already have one
                    positions = trading_service.get_open_positions()
                    symbols_in_position = [position.symbol for position in positions]
                    if symbol not in symbols_in_position:
                        take_profit_price = price * (1 + TAKE_PROFIT_PERCENTAGE)
                        stop_loss_price = price * (1 - STOP_LOSS_PERCENTAGE)
                        trading_service.place_bracket_order(symbol, qty, take_profit_price, stop_loss_price)
        time.sleep(60)  # Wait for 1 minute before checking again

def menu(trading_service, data_service):
    """Display menu options to the user."""
    while True:
        print("\nMenu:")
        print("1. Obtain Profits (Close all positions)")
        print("2. Status (Show current margin of positions)")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            # Close all positions
            positions = trading_service.get_open_positions()
            if positions:
                for position in positions:
                    trading_service.close_position(position.symbol)
                print("All positions have been closed.")
            else:
                print("No open positions to close.")
        elif choice == '2':
            # Show current margin of positions
            positions = trading_service.get_open_positions()
            if positions:
                print("Current Positions:")
                for position in positions:
                    print(f"Symbol: {position.symbol}, Qty: {position.qty}, Current Price: {position.current_price}, Market Value: {position.market_value}")
            else:
                print("No open positions.")
        elif choice == '3':
            print("Exiting...")
            exit(0)
        else:
            print("Invalid choice. Please try again.")

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    trading_service = TradingService()
    data_service = DataService()

    # Start the idle mode in a separate thread
    idle_thread = threading.Thread(target=idle_mode, args=(trading_service, data_service), daemon=True)
    idle_thread.start()

    # Start the menu
    menu(trading_service, data_service)

if __name__ == '__main__':
    main()
