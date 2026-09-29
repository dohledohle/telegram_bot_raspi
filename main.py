import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from rpi_lcd import LCD

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
lcd = LCD()

async def handle_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    await context.bot.send_message(chat_id=update.message.chat_id, text="Hallo Welt!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, handle_update))
app.run_polling()

