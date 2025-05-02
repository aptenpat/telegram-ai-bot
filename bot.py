import os
import openai
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.ext import Dispatcher, CallbackContext

# Токены
TELEGRAM_BOT_TOKEN = os.getenv("7604837388:AAGJnvQIG-F5xbcAMnBf-5XjMsD9vzO6X7o")
OPENAI_API_KEY = os.getenv("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")

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Настройка Flask
app = Flask(__name__)

# Создание бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Получаем порт из переменных окружения, если он есть (для Render)
PORT = int(os.environ.get("PORT", 10000))

# Инициализация ApplicationBuilder для обработки сообщений
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я ИИ-бот. Напиши мне сообщение, и я постараюсь ответить умно 🙂")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        answer = response['choices'][0]['message']['content'].strip()
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("Ошибка при запросе к ИИ 😢")
        print(f"Ошибка OpenAI: {e}")

# Настройка webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    # Получаем данные от Telegram
    json_str = request.get_data().decode('UTF-8')
    update = Update.de_json(json_str, bot)
    
    # Диспетчер для обработки входящих сообщений
    dispatcher = Dispatcher(bot, None)
    
    # Добавляем обработчики команд и сообщений
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обрабатываем update
    dispatcher.process_update(update)
    return '', 200

# Установка webhook на сервер Telegram
def set_webhook():
    webhook_url = f"https://telegram-ai-bot-p30m.onrender.com"  # Укажи URL своего сервера на Render
    bot.set_webhook(webhook_url)

# Запуск Flask
if __name__ == '__main__':
    # Устанавливаем webhook при запуске
    set_webhook()
    
    # Запуск Flask сервера
    app.run(host='0.0.0.0', port=PORT)