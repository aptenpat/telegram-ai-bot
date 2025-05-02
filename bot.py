import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.ext import Updater
from dotenv import load_dotenv

# Загружаем токены из переменных окружения
print("OPENAI_API_KEY:", os.environ.get("OPENAI_API_KEY"))
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
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
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен!")

    # Запуск бота с учетом порта, чтобы он мог работать на Render
    # Для Render нужно либо использовать webhook, либо polling. В данном примере используем polling.
    app.run_polling()