import asyncio
import textwrap
from telegram import Update
from telegram.ext import ContextTypes
from hardware import lcd
import random

last_chat_id = None
backlight_on = True
current_text = None
dim_timer = None

timeout_seconds = 15

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
    await context.bot.send_message(chat_id=update.message.chat_id,
                                   text=random.choice(antworten))

async def display_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_chat_id, current_text, backlight_on, dim_timer
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
    lcd.backlight(True)
    backlight_on = True
    lcd.text(zeile1, 1)
    lcd.text(zeile2, 2)

    if dim_timer is not None:
        dim_timer.cancel()
    dim_timer = asyncio.create_task(auto_darkmode())

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
    await update.message.reply_text(f"Beleuchtung: {beleuchtung}\nAngezeigter "
                                    f"Text: {text_status}")

async def auto_darkmode():
    global backlight_on
    try:
        await asyncio.sleep(timeout_seconds)
        lcd.backlight(False)
        backlight_on = False
    except asyncio.CancelledError:
        pass

def turn_on_backlight(): #Hilfsfunktion, wird vom Nutzer nicht direkt aufgerufen
    global backlight_on
    backlight_on = True
    lcd.backlight(True)

def start_dim_timer(): #Brücke, um Timer zurückzusetzen, nachdem Bildschirm aufgeweckt
    global dim_timer
    if dim_timer is not None:
        dim_timer.cancel()
    dim_timer = asyncio.create_task(auto_darkmode())