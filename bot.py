import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai

# Получаем токен из переменной окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Выводим токен в логи для отладки (убедитесь, что логирование безопасно и токен не попадет в чужие руки)
print(f"Telegram Token: {TELEGRAM_TOKEN}")

# Инициализируем бота с использованием токена
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Устанавливаем ключ API для OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context) -> None:
    await update.message.reply_text('Привет! Задавай свои вопросы.')

# Обработчик сообщений для общения с ChatGPT
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

# Запускаем бота
if __name__ == '__main__':
    app.run_polling()
