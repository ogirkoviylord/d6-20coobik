# D6/D20 Telegram Bot + 'да' Trigger

Функции:
- `/d6` → 1..6
- `/d20` → 1..20
- Текстовые триггеры: `д6`, `d6`, `д20`, `d20` (в группах без слеша, если privacy выключен у бота).
- Если пользователь пишет **ровно** `да` (любой регистр; допустимы `. ! ? …` в конце) — бот отвечает `пизда`.
- Можно ограничить реакцию на `да` ТОЛЬКО для конкретных пользователей: переменная `TARGET_USER_IDS` (через запятую).

## Переменные окружения
- `TELEGRAM_BOT_TOKEN` — токен из @BotFather (обязательно).
- `TARGET_USER_IDS` — необязательно. Пример: `123456789,987654321`.

## Локально
```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=ТОКЕН
# (опц.) export TARGET_USER_IDS=123456789,987654321
python main.py
```

## Railway (Docker)
1. Залей файлы в GitHub.
2. Railway → New Project → Deploy from GitHub.
3. В **Variables** добавь `TELEGRAM_BOT_TOKEN` (+ опц. `TARGET_USER_IDS`).
4. Проверяй бота: `/start`, `/d6`, `/d20`.
5. Для `д6`/`д20` как текст в группах — в @BotFather: `/setprivacy` → Disable.