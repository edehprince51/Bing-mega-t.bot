import os
import logging
import MetaTrader5 as mt5
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from binance.spot import Spot as BinanceClient
from dotenv import load_dotenv

load_dotenv()

class ProfessionalTradingBot:
    def __init__(self):
        self.is_active = False
        self.binance_client = BinanceClient(api_key=os.getenv("BINANCE_API_KEY"))
        
    async def init_mt5(self):
        """Initializes connection to MT5 terminal."""
        if not mt5.initialize():
            return False
        return mt5.login(
            int(os.getenv("MT5_LOGIN")), 
            password=os.getenv("MT5_PASSWORD"), 
            server=os.getenv("MT5_SERVER")
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.is_active = True
        await update.message.reply_text("🚀 Bot Online. Monitoring Pocket Option & MT5 assets...")

    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        connected = await self.init_mt5()
        msg = "💹 **Account Balances**\n"
        if connected:
            acc = mt5.account_info()
            msg += f"• MT5: ${acc.balance}\n"
        # Placeholder for PO WebSocket balance retrieval
        msg += f"• Pocket Option UID: {os.getenv('PO_UID')}\n"
        await update.message.reply_text(msg, parse_mode='Markdown')

if __name__ == "__main__":
    bot = ProfessionalTradingBot()
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CommandHandler("balance", bot.balance))
    
    print("Bot is listening for commands...")
    app.run_polling()
