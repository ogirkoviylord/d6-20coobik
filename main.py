import os
import re
import random
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    AIORateLimiter,
    defaults,
    filters,
)

# --- Logging (visible in Railway Logs) ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("d6-d20-bot")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # set in Railway Variables

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я D6-bot (+ D20).\n"
        "Команды: /d6 и /d20.\n"
        "В группах могу реагировать на 'д6' или 'д20' без слеша — если в @BotFather выключен privacy."
    )

async def roll_d6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = random.randint(1, 6)
    await update.message.reply_text(f"🎲 (D6) Выпало: {result}")

async def roll_d20(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = random.randint(1, 20)
    await update.message.reply_text(f"🎲 (D20) Выпало: {result}")

# --- Text triggers (ловим д6/d6/д20/d20 и даже с ведущим / как текст) ---
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
    # Register bot commands (only latin commands are valid in Telegram)
    await app.bot.set_my_commands([
        ("d6", "Бросить шестигранный кубик"),
        ("d20", "Бросить двадцатигранный кубик"),
    ])
    me = await app.bot.get_me()
    log.info("Bot started as @%s (id=%s)", me.username, me.id)

def main() -> None:
    if not TOKEN:
        raise RuntimeError("Не найден TELEGRAM_BOT_TOKEN. Задай переменную окружения на Railway.")

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .rate_limiter(AIORateLimiter())
        .defaults(defaults.Defaults(block=False))
        .build()
    )

    # Commands (only latin command names are allowed)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("d6", roll_d6))
    app.add_handler(CommandHandler("d20", roll_d20))

    # Text triggers (для 'д6' и 'д20' без слеша, если privacy отключен)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    # Long polling
    app.run_polling(allowed_updates=["message", "edited_message", "callback_query"])

if __name__ == "__main__":
    main()