import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import argparse

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        try:
            # Test connectivity
            self.client.futures_ping()
            logging.info("Connected to Binance Futures Testnet successfully.")
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            raise

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            params = {
                'symbol': symbol,
                'side': SIDE_BUY if side == 'buy' else SIDE_SELL,
                'type': order_type,
                'quantity': quantity,
            }
            if order_type == ORDER_TYPE_LIMIT:
                params.update({
                    'price': price,
                    'timeInForce': TIME_IN_FORCE_GTC
                })

            logging.info(f"Placing order: {params}")
            order = self.client.futures_create_order(**params)
            logging.info(f"Order placed: {order}")
            return order
        except BinanceAPIException as e:
            logging.error(f"Binance API error: {e.message}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")


def get_args():
    parser = argparse.ArgumentParser(description="Simple Binance Futures Bot")
    parser.add_argument('--symbol', required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument('--side', required=True, choices=['buy', 'sell'], help="Order side")
    parser.add_argument('--type', required=True, choices=['MARKET', 'LIMIT'], help="Order type")
    parser.add_argument('--quantity', required=True, type=float, help="Order quantity")
    parser.add_argument('--price', type=float, help="Price (required for LIMIT orders)")
    return parser.parse_args()


if __name__ == "__main__":
    # TODO: Replace with your testnet credentials
    API_KEY = ""
    API_SECRET = ""

    args = get_args()

    bot = BasicBot(API_KEY, API_SECRET)
    bot.place_order(
        symbol=args.symbol.upper(),
        side=args.side.lower(),
        order_type=ORDER_TYPE_LIMIT if args.type == 'LIMIT' else ORDER_TYPE_MARKET,
        quantity=args.quantity,
        price=args.price
    )
