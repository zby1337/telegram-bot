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

TOKEN = os.getenv("TOKEN")

CHAT_IDS = [
    "727169692",
    "5020135485",
    "624884275",
    "-1002758054105"
]


# =========================
# GET JOKE
# =========================

def get_joke():

    url = "https://www.anekdot.ru/random/anekdot/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        joke = soup.find(
            "div",
            class_="text"
        )

        if joke:
            return joke.get_text(strip=True)

    except Exception as e:
        print(f"Ошибка получения анекдота: {e}")

    return "Анекдот не найден 😢"


# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "This bot talkinn someshi 4 no reason"
    )


async def nasral(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        get_joke()
    )


# =========================
# AUTO SEND
# =========================

async def auto_send(app):

    while True:

        joke = get_joke()

        for chat_id in CHAT_IDS:

            try:

                await app.bot.send_message(
                    chat_id=chat_id,
                    text=joke
                )

                print(f"Отправлено в {chat_id}")

            except Exception as e:

                print(f"Ошибка отправки: {e}")

        await asyncio.sleep(3600)


# =========================
# MAIN
# =========================

async def main():

    if not TOKEN:
        raise ValueError("TOKEN not found")

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("nasral", nasral)
    )

    print("Bot started")

    asyncio.create_task(
        auto_send(app)
    )

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


# =========================
# START
# =========================

if __name__ == "__main__":

    asyncio.run(main())