import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai

# Получаем токен из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Устанавливаем ключ API для OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Инициализируем бота с использованием токена
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Команда /start
async def start(update: Update, context) -> None:
    await update.message.reply_text('Привет! Задавай свои вопросы.')

# Обработка сообщений для общения с ChatGPT
async def chatgpt(update: Update, context) -> None:
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ]
        )
        answer = response['choices'][0]['message']['content'].strip()
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f'Ошибка: {str(e)}')

# Добавляем обработчики команд и сообщений
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt))

# Запускаем бота с использованием вебхука
if __name__ == '__main__':
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TELEGRAM_TOKEN}"
    )
