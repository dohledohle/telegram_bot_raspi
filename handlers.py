import textwrap
from telegram import Update
from telegram.ext import ContextTypes
from hardware import lcd
import random

last_chat_id = None
backlight_on = True
current_text = None

antworten = [
    "Da bin ich!",
    "Ja, bitte?",
    "Huhu!",
    "Was gibt's?",
    "Moin!",
    "Was kann ich für dich tun?",
    "Wollen wir eine Nachricht senden?",
    "Was treibt dich um?",
    "Ja?",
    "Hey!",
    "Ich bin ganz Ohr :)",
    "Was wollen wir tun?",
    "Hallo, da bin ich?",
    "Stets zu Diensten!",
    "Woran denkst du?"
]

async def handle_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    await context.bot.send_message(chat_id=update.message.chat_id, text=random.choice(antworten))

async def display_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_chat_id, current_text
    last_chat_id = update.message.chat_id

    if not context.args:
        await update.message.reply_text("Bitte gib einen Text ein, zB so: "
                                        "'/display Das ist ein Text!'")
        return

    text = " ".join(context.args)
    current_text = text
    zeilen = textwrap.wrap(text, width=16)

    zeile1 = zeilen[0] if len(zeilen) > 0 else ""
    zeile2 = zeilen[1] if len(zeilen) > 1 else ""

    lcd.clear()
    lcd.text(zeile1, 1)
    lcd.text(zeile2, 2)

    await update.message.reply_text("Auf dem Display angezeigt!")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_text
    lcd.clear()
    current_text = None
    await update.message.reply_text("Display zurückgesetzt!")

async def lightmode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global backlight_on
    lcd.backlight(True)
    backlight_on = True
    await update.message.reply_text("Display eingeschaltet!")

async def darkmode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global backlight_on
    lcd.backlight(False)
    backlight_on = False
    await update.message.reply_text("Display ausgeschaltet!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    beleuchtung = "an" if backlight_on else "aus"
    text_status = f"'{current_text}'" if current_text else "kein Text"
    await update.message.reply_text(f"Beleuchtung: {beleuchtung}\nAngezeigter Text: {text_status}")