import asyncio
import requests
from bs4 import BeautifulSoup

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

TOKEN = "8642180301:AAEyx8FihXqLgk0gxwCsdqZmnWyTb3Is4rw"
CHAT_IDS = ["727169692", "5020135485", "624884275","-1002758054105"]

# ===== ПОЛУЧЕНИЕ АНЕКДОТА =====

def get_joke():

    url = "https://www.anekdot.ru/random/anekdot/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    joke = soup.find("div", class_="text")

    if joke:
        return joke.get_text(strip=True)

    return "Анекдот не найден 😢"

# ===== КОМАНДА START =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "This bot talking someshit for no reason 🙂"
    )

    await update.message.reply_text(text)

# ===== КОМАНДА JOKE =====

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = get_joke()

    await update.message.reply_text(text)

# ===== АВТОРАССЫЛКА =====

async def auto_send(app):

    while True:

        for chat_id in CHAT_IDS:

            text = get_joke()

            await app.bot.send_message(
                chat_id=chat_id,
                text=text
            )

        print("Анекдоты отправлены")

        await asyncio.sleep(3600)

# ===== ЗАПУСК =====

# запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("nasral", joke))

import asyncio
asyncio.get_event_loop().create_task(auto_send(app))

print("Bot started")
app.run_polling()