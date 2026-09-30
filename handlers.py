import textwrap
from telegram import Update
from telegram.ext import ContextTypes
from hardware import lcd

last_chat_id = None

async def handle_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    await context.bot.send_message(chat_id=update.message.chat_id, text="Da bin ich!")

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

async def lightmode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lcd.backlight(True)
    await update.message.reply_text("Display eingeschaltet!")

async def darkmode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lcd.backlight(False)
    await update.message.reply_text("Display ausgeschaltet!")