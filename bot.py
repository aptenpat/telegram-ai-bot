import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.ext import Updater

# Загружаем токены из переменных окружения
print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
TELEGRAM_BOT_TOKEN = "7604837388:AAGaUO2kP_a_yBfKVYD3VeezVNG3H1V4YJU"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# Получаем порт из переменных окружения, если он есть (для Render)
PORT = int(os.environ.get("PORT", 10000))

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я ИИ-бот. Напиши мне сообщение, и я постараюсь ответить умно 🙂")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150,
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("Ошибка при запросе к ИИ 😢")
        print(f"Ошибка OpenAI: {e}")

# Запуск приложения
if __name__ == "__main__":
    # Используем ApplicationBuilder для запуска бота
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Добавляем обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")

    # Запуск бота с учетом порта, чтобы он мог работать на Render
    # Для Render нужно либо использовать webhook, либо polling. В данном примере используем polling.
    app.run_polling()