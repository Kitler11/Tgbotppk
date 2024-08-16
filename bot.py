from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai

# Вставь сюда токен Telegram
TELEGRAM_TOKEN = "Telegram_token"
# Вставь сюда ключ API от OpenAI
OPENAI_API_KEY = "Your_api_key"
openai.api_key = OPENAI_API_KEY

async def start(update: Update, context) -> None:
    await update.message.reply_text('Привет! Задавай свои вопросы.')

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

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt))

    app.run_polling()
