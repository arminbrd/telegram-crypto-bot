from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pycoingecko import CoinGeckoAPI
import os

# Get token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

# Initialize CoinGecko API client
cg = CoinGeckoAPI()

def get_crypto_price(crypto):
    try:
        data = cg.get_price(ids=crypto, vs_currencies=['usd', 'irr'])  # استفاده از IRR برای تومان ایران
        price_usd = data.get(crypto, {}).get('usd', None)
        price_irr = data.get(crypto, {}).get('irr', None)  # قیمت به تومان (ریال ایران)
        return price_usd, price_irr
    except Exception as e:
        return None, None

def ez(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text("Please provide the cryptocurrency symbol. Example: /ez BTC")
        return

    crypto_symbol = context.args[0].lower()
    price_usd, price_irr = get_crypto_price(crypto_symbol)

    if price_usd is not None:
        update.message.reply_text(f"💰 The price of {crypto_symbol.upper()} is:\n"
                                  f"USD: ${price_usd}\n"
                                  f"IRR: ﷼{price_irr}")
    else:
        update.message.reply_text("❌ Cryptocurrency not found or there is an issue.")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hello! To get cryptocurrency prices, use the following commands:\n\n"
                              "/ez BTC\n"
                              "/ez ETH")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ez", ez))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
