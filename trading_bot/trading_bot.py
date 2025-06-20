import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

# ✅ Fix for STOP_MARKET not being included in some versions
ORDER_TYPE_STOP_MARKET = 'STOP_MARKET'

# ✅ Configure logging
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.base_url = "https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com"
        self.client = Client(api_key, api_secret)
        self.client.FUTURES_URL = f"{self.base_url}/fapi"  # ✅ Correct testnet path
        logging.info("Initialized Binance Futures Client with Testnet = %s", testnet)

    def is_valid_symbol(self, symbol):
        try:
            info = self.client.futures_exchange_info()
            valid_symbols = [s['symbol'] for s in info['symbols']]
            return symbol in valid_symbols
        except Exception as e:
            logging.error("Error validating symbol: %s", e)
            return False

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            params = {
                'symbol': symbol,
                'side': SIDE_BUY if side == 'BUY' else SIDE_SELL,
                'type': order_type,
                'quantity': quantity
            }

            if order_type == ORDER_TYPE_LIMIT:
                params['timeInForce'] = TIME_IN_FORCE_GTC
                params['price'] = float(price)

            elif order_type == ORDER_TYPE_STOP or order_type == ORDER_TYPE_STOP_MARKET:
                params['stopPrice'] = float(stop_price)
                if order_type == ORDER_TYPE_STOP:
                    params['price'] = float(price)
                    params['timeInForce'] = TIME_IN_FORCE_GTC

            order = self.client.futures_create_order(**params)

            logging.info("Order placed: %s", order)
            print("✅ Order placed successfully! ID:", order['orderId'])
            return order

        except BinanceAPIException as e:
            logging.error("Binance API Error: %s", e)
            print("❌ Binance API Error:", e)
        except Exception as e:
            logging.error("General Error: %s", e)
            print("❌ Error placing order:", e)


# ✅ CLI Interface
if __name__ == "__main__":
    print("\nWelcome to the Binance Futures Testnet Trading Bot 🚀")

    api_key = input("Enter your Binance API Key: ").strip()
    api_secret = input("Enter your Binance API Secret: ").strip()

    bot = BasicBot(api_key, api_secret)

    while True:
        print("\n--- New Trade ---")
        symbol = input("Symbol (e.g., BTCUSDT): ").upper().strip()

        if not bot.is_valid_symbol(symbol):
            print("❌ Invalid symbol. Please check and try again.")
            continue

        side = input("Side (BUY or SELL): ").upper().strip()
        if side not in ["BUY", "SELL"]:
            print("❌ Invalid side. Please enter BUY or SELL.")
            continue

        order_type_input = input("Order Type (MARKET / LIMIT / STOP_LIMIT): ").upper().strip()
        quantity = input("Quantity: ").strip()
        try:
            quantity = float(quantity)
        except ValueError:
            print("❌ Invalid quantity. Please enter a number.")
            continue

        price = None
        stop_price = None

        if order_type_input == "LIMIT":
            price = input("Enter Limit Price: ").strip()
            try:
                price = float(price)
            except ValueError:
                print("❌ Invalid price. Please enter a number.")
                continue
            order_type = ORDER_TYPE_LIMIT

        elif order_type_input == "STOP_LIMIT":
            stop_price = input("Enter Stop Price: ").strip()
            price = input("Enter Limit Price (after stop is hit): ").strip()
            try:
                stop_price = float(stop_price)
                price = float(price)
            except ValueError:
                print("❌ Invalid stop price or limit price. Please enter numbers.")
                continue
            order_type = ORDER_TYPE_STOP  # Binance treats stop-limit as STOP

        elif order_type_input == "MARKET":
            order_type = ORDER_TYPE_MARKET

        else:
            print("❌ Invalid order type. Please use MARKET, LIMIT, or STOP_LIMIT.")
            continue

        bot.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price
        )

        again = input("\nDo you want to place another order? (y/n): ").lower()
        if again != 'y':
            print("✅ Thank you! Exiting bot.")
            break
