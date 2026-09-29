import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from rpi_lcd import LCD

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
lcd = LCD()


async def handle_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    await context.bot.send_message(chat_id=update.message.chat_id, text="Da bin ich!")

async def display_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lcd.text("Hey!", 1)
    lcd.text("Hab dich lieb :)", 2)
    await update.message.reply_text("Auf dem Display angezeigt!")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_update))
app.add_handler(CommandHandler("display", display_command))
app.run_polling()