import os
import re
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# --- Logging (visible on Railway) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("d6d20-bot")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # set this env var on Railway

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я D6/D20 бот.\n"
        "Команды: /d6 и /d20.\n"
        "В группах могу реагировать на 'д6' или 'д20' без слеша — если в @BotFather выключен privacy."
    )

async def roll_d6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"🎲 (D6) Выпало: {random.randint(1, 6)}")

async def roll_d20(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"🎲 (D20) Выпало: {random.randint(1, 20)}")

# ловим 'д6'/'d6'/'д20'/'d20' (и даже с ведущим '/'), если privacy отключён
DICE_REGEX = re.compile(r"^\s*[\/]?(?:д6|d6|д20|d20)\s*$", re.IGNORECASE)

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if not msg or not msg.text:
        return
    txt = msg.text.strip().lower()
    if DICE_REGEX.match(txt):
        if "20" in txt:
            await roll_d20(update, context)
        else:
            await roll_d6(update, context)

async def post_init(app: Application) -> None:
    await app.bot.set_my_commands([
        ("d6", "Бросить шестигранный кубик"),
        ("d20", "Бросить двадцатигранный кубик"),
    ])
    me = await app.bot.get_me()
    log.info("Bot started as @%s (id=%s)", me.username, me.id)

def main() -> None:
    if not TOKEN:
        raise RuntimeError("Не найден TELEGRAM_BOT_TOKEN. Задай переменную окружения.")

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    # Commands (ONLY latin names allowed by Telegram)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("d6", roll_d6))
    app.add_handler(CommandHandler("d20", roll_d20))

    # Text triggers (for 'д6'/'д20' without slash in groups if privacy is disabled)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()