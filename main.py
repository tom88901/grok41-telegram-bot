import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import threading

app = Flask(__name__)

# OpenRouter key
OPENROUTER_KEY = os.environ['OPENROUTER_KEY']
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

# Webhook endpoint cho Telegram
@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), None)
    application.process_update(update)
    return 'OK'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Địt mẹ gửi tin nhắn đi bố, tao trả lời bằng Grok 4.1 Fast siêu dâm đây 🔥")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.reply_chat_action("typing")

    payload = {
        "model": "x-ai/grok-4.1-fast",
        "messages": [{"role": "user", "content": user_msg}],
        "temperature": 0.9,
        "max_tokens": 4096
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://render.com",
        "X-Title": "Grok41Fast Dâm Bot",
        "Content-Type": "application/json"
    }

    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=90)
        reply = r.json()["choices"][0]["message"]["content"]
        if len(reply) > 4096:
            for i in range(0, len(reply), 4096):
                await update.message.reply_text(reply[i:i+4096])
        else:
            await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Lỗi rồi thằng lồn: {e}")

application = Application.builder().token(TELEGRAM_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

# Chạy Flask
if __name__ == '__main__':
    # Set webhook (chạy 1 lần khi deploy)
    application.bot.set_webhook(url=f"https://your-app-name.onrender.com/{TELEGRAM_TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
