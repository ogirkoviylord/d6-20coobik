# D6 + D20 Telegram Bot — Railway + Docker

Команды:
- `/d6` — бросок 1..6
- `/d20` — бросок 1..20

Текстовые триггеры (если privacy выключен в @BotFather): `д6`, `d6`, `д20`, `d20`.

## Локально
```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=ТОКЕН  # Windows: set TELEGRAM_BOT_TOKEN=...
python main.py
```

## Railway (Docker)
1. Залей файлы в GitHub (или используй Railway CLI).
2. На railway.app: New Project → Deploy from GitHub → выбери репозиторий.
3. В **Variables** добавь `TELEGRAM_BOT_TOKEN`.
4. После билда открой бота: `/start`, `/d6`, `/d20`.