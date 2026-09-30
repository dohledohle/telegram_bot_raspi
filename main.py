import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from hardware import lcd, button
import textwrap
import asyncio

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
last_chat_id = None
event_loop = None

async def send_read_receipt():
    if last_chat_id is not None:
        await app.bot.send_message(chat_id=last_chat_id, text="Nachricht wurde gelesen!")

def button_pressed():
    if event_loop is not None:
        asyncio.run_coroutine_threadsafe(send_read_receipt(), event_loop)


async def handle_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text="Da bin ich!")

async def display_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_chat_id
    last_chat_id = update.message.chat_id

    if not context.args:
        await update.message.reply_text("Bitte gib einen Text ein, zB so: "
                                        "'/display Das ist ein Text!'")
        return

    text = " ".join(context.args)
    zeilen = textwrap.wrap(text, width=16)

    zeile1 = zeilen[0] if len(zeilen) > 0 else ""
    zeile2 = zeilen[1] if len(zeilen) > 1 else ""

    lcd.clear()
    lcd.text(zeile1, 1)
    lcd.text(zeile2, 2)

    await update.message.reply_text("Auf dem Display angezeigt!")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lcd.clear()
    await update.message.reply_text("Display zurückgesetzt!")

async def setup(application):
    global event_loop
    event_loop = asyncio.get_running_loop()

button.when_pressed = button_pressed

app = ApplicationBuilder().token(TOKEN).post_init(setup).build()
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_update))
app.add_handler(CommandHandler("clear", clear_command))
app.add_handler(CommandHandler("display", display_command))
app.run_polling()