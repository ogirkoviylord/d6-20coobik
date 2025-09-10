import os
import re
import random
import logging
from typing import Set

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("d6d20-bot")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # обязательно задай в Railway Variables

# Необязательная настройка таргета:
# Если переменная окружения TARGET_USER_IDS задана (через запятую, ИДшники Telegram),
# бот будет отвечать на 'да' ТОЛЬКО этим пользователям.
# Пример: TARGET_USER_IDS=123456789,987654321
def parse_target_ids(env_val: str | None) -> Set[int]:
    if not env_val:
        return set()
    out: Set[int] = set()
    for part in env_val.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.add(int(part))
        except ValueError:
            log.warning("Некорректный user id в TARGET_USER_IDS: %r", part)
    return out

TARGET_USER_IDS = parse_target_ids(os.getenv("TARGET_USER_IDS"))

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я D6/D20 бот с триггером на 'да'.\n"
        "Команды: /d6 и /d20.\n"
        "Пишешь 'д6' или 'д20' — тоже брошу (если privacy выключен).\n"
        "Если сообщение — ровно 'да' (в любом регистре, с точкой/!/?) — отвечу грубостью.\n"
        "Можно ограничить реакцию на 'да' только для конкретных пользователей через переменную TARGET_USER_IDS."
    )

async def roll_d6(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"🎲 (D6) Выпало: {random.randint(1, 6)}")

async def roll_d20(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"🎲 (D20) Выпало: {random.randint(1, 20)}")

# ловим 'д6'/'d6'/'д20'/'d20' (и даже с ведущим '/'), если privacy отключён
DICE_REGEX = re.compile(r"^\s*[\/]?(?:д6|d6|д20|d20)\s*$", re.IGNORECASE)

# 'да' (только кириллица), любые пробелы вокруг, допускаем . ! ? … многоточие
YES_REGEX = re.compile(r"^\s*да[.!?…]*\s*$", re.IGNORECASE)

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if not msg or not msg.text:
        return

    txt = msg.text.strip()

    # 1) DICE text triggers
    if DICE_REGEX.match(txt.lower()):
        if "20" in txt:
            await roll_d20(update, context)
        else:
            await roll_d6(update, context)
        return

    # 2) YES trigger ('да' only)
    if YES_REGEX.match(txt):
        user = update.effective_user
        if TARGET_USER_IDS and user and user.id not in TARGET_USER_IDS:
            return  # ограничение включено и пользователь не в списке
        # Ответить автору грубостью
        await msg.reply_text("пизда")
        return

async def post_init(app: Application) -> None:
    await app.bot.set_my_commands([
        ("d6", "Бросить шестигранный кубик"),
        ("d20", "Бросить двадцатигранный кубик"),
    ])
    me = await app.bot.get_me()
    log.info("Bot started as @%s (id=%s). Targets: %s", me.username, me.id,
             ",".join(str(i) for i in sorted(TARGET_USER_IDS)) if TARGET_USER_IDS else "ALL")

def main() -> None:
    if not TOKEN:
        raise RuntimeError("Не найден TELEGRAM_BOT_TOKEN. Задай переменную окружения.")

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("d6", roll_d6))
    app.add_handler(CommandHandler("d20", roll_d20))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()