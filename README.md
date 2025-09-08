# D6/D20 Telegram Bot — Clean Build (PTB v21.6)

Команды:
- `/d6` — бросок 1..6
- `/d20` — бросок 1..20

Текстовые триггеры: `д6`, `d6`, `д20`, `d20` (работают в группах без слеша, если у бота выключен privacy в @BotFather).

## Локально
```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN=ТОКЕН  # Windows: set TELEGRAM_BOT_TOKEN=ТОКЕН
python main.py
```

## Railway (Docker)
1. Залей файлы в GitHub-репозиторий.
2. На railway.app: New Project → Deploy from GitHub → выбери репо.
3. В Variables добавь `TELEGRAM_BOT_TOKEN`.
4. После старта проверяй бота: `/start`, `/d6`, `/d20`.