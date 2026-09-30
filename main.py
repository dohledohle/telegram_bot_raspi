import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from hardware import button
import handlers
import asyncio

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
event_loop = None

async def send_read_receipt():
    if handlers.last_chat_id is not None:
        await app.bot.send_message(chat_id=handlers.last_chat_id, text="Nachricht wurde gelesen!")

def button_pressed():
    if event_loop is not None:
        asyncio.run_coroutine_threadsafe(send_read_receipt(), event_loop)

async def setup(application):
    global event_loop
    event_loop = asyncio.get_running_loop()

button.when_pressed = button_pressed

app = ApplicationBuilder().token(TOKEN).post_init(setup).build()
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handlers.handle_update))
app.add_handler(CommandHandler("clear", handlers.clear_command))
app.add_handler(CommandHandler("display", handlers.display_command))
app.run_polling()