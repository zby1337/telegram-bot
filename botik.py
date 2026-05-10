from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

import requests
from bs4 import BeautifulSoup
import asyncio
import os
import threading
from flask import Flask

TOKEN = os.getenv("TOKEN")

CHAT_IDS = [
    "727169692",
    "5020135485",
    "624884275",
    "-1002758054105"
]

# =========================
# WEB SERVER (FOR RENDER)
# =========================

app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "bot is alive"


def run_server():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)


# =========================
# JOKE
# =========================

def get_joke():
    url = "https://www.anekdot.ru/random/anekdot/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        joke = soup.find("div", class_="text")

        if joke:
            return joke.get_text(strip=True)

    except Exception as e:
        print(f"Error: {e}")

    return "Анекдот не найден 😢"


# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This bot talkinn someshi 4 no reason")


async def nasral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_joke())


# =========================
# AUTO SEND
# =========================

async def auto_send(app):

    while True:

        joke = get_joke()

        for chat_id in CHAT_IDS:
            try:
                await app.bot.send_message(chat_id=chat_id, text=joke)
                print(f"Sent to {chat_id}")
            except Exception as e:
                print(f"Error: {e}")

        await asyncio.sleep(3600)


# =========================
# MAIN
# =========================

def main():

    if not TOKEN:
        raise ValueError("TOKEN not found")

    # запускаем веб-сервер (ВАЖНО для Render)
    threading.Thread(target=run_server, daemon=True).start()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nasral", nasral))

    print("Bot started")

    # безопасный запуск фоновой задачи
    async def runner():
        await auto_send(app)

    asyncio.get_event_loop().create_task(runner())

    app.run_polling(drop_pending_updates=True)


# =========================
# START
# =========================

if __name__ == "__main__":
    main()