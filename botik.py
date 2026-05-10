import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# =========================
# LOAD ENV
# =========================

load_dotenv()

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN не загружен! Проверь .env файл")

# =========================
# CHAT IDS
# =========================

CHAT_IDS = [
    "727169692",
    "5020135485",
    "624884275",
    "-1002758054105"
]

# =========================
# JOKE FUNCTION
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
        print(f"Ошибка получения анекдота: {e}")

    return "Анекдот не найден 😢"


# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "This bot talking someshit for no reason 🙂"
    )


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_joke())


# =========================
# AUTO SEND (JOB QUEUE)
# =========================

async def send_jokes(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in CHAT_IDS:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=get_joke()
            )
        except Exception as e:
            print(f"Ошибка отправки в {chat_id}: {e}")

    print("Анекдоты отправлены")


# =========================
# MAIN
# =========================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nasral", joke))

    # авто-рассылка каждые 3600 секунд (1 час)
    job_queue = app.job_queue
    job_queue.run_repeating(send_jokes, interval=3600, first=10)

    print("Bot started")

    # ВАЖНО: без asyncio.run
    app.run_polling()


# =========================
# START
# =========================

if __name__ == "__main__":
    main()