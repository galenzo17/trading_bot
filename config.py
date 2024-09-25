# config.py

API_KEY = 'YOUR_ALPACA_API_KEY'
SECRET_KEY = 'YOUR_ALPACA_SECRET_KEY'
BASE_URL = 'https://paper-api.alpaca.markets'  # Use paper trading for testing

# List of stocks to monitor
STOCKS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Trading parameters
MAX_POSITION_SIZE = 1000  # Maximum dollar amount to invest per trade
TAKE_PROFIT_PERCENTAGE = 0.02  # 2% profit target
STOP_LOSS_PERCENTAGE = 0.01  # 1% stop loss
