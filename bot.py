import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai
from openai import OpenAI

TELEGRAM_TOKEN = '6891639004:AAG8GtAbAlHJ94f-yiBHfPraA3wuCGagXaU'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация бота
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

client = OpenAI(
  # This is the default and can be omitted
  api_key=OPENAI_API_KEY,
)

# Команда /start
async def start(update: Update, context) -> None:
    await update.message.reply_text('Привет! Задавай свои вопросы.')

# Обработка сообщений для общения с ChatGPT
async def chatgpt(update: Update, context) -> None:
    user_message = update.message.text
    try:
        chat_completion = client.chat.completions.create(
          messages=[
            {
              "role": "user",
              "content": "Say this is a test",
            }
          ],
          model="gpt-3.5-turbo",
        )
        print(chat_completion)
        answer = chat_completion.choices[0].message['content']
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

# Добавление обработчиков команд и сообщений
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt))

if __name__ == '__main__':
    app.run_polling()










# import os
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
# import openai

# TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# openai.api_key = OPENAI_API_KEY

# # Инициализация бота
# app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# # Команда /start
# async def start(update: Update, context) -> None:
#     await update.message.reply_text('Привет! Задавай свои вопросы.')

# # Обработка сообщений для общения с ChatGPT
# async def chatgpt(update: Update, context) -> None:
#     user_message = update.message.text
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": user_message},
#             ],
#         )
#         answer = response.choices[0].message['content'].strip()
#         await update.message.reply_text(answer)
#     except Exception as e:
#         await update.message.reply_text(f"Ошибка: {str(e)}")

# # Добавление обработчиков команд и сообщений
# app.add_handler(CommandHandler('start', start))
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt))

# if __name__ == '__main__':
#     app.run_polling()
