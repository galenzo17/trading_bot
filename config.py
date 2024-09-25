# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = os.getenv('BASE_URL')

# List of stocks to monitor
STOCKS = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']

# Trading parameters
MAX_POSITION_SIZE = 10  # Maximum dollar amount to invest per trade
TAKE_PROFIT_PERCENTAGE = 0.02  # 2% profit target
STOP_LOSS_PERCENTAGE = 0.01  # 1% stop loss
