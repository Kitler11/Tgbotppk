import os
from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from openai import OpenAI
import requests
import json

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Yandex GPT
CATALOG_ID     = os.getenv("CATALOG_ID")
SECRET_KEY     = os.getenv("SECRET_KEY")

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
# async def chatgpt(update: Update, context) -> None:
#     user_message = update.message.text
#     try:
#         chat_completion = client.chat.completions.create(
#           messages=[
#             {
#               "role": "user",
#               "content": user_message,
#             }
#           ],
#           model="gpt-3.5-turbo",
#         )
#         print(chat_completion)
#         answer = chat_completion.choices[0].message['content']
#         await update.message.reply_text(answer)
#     except Exception as e:
#         await update.message.reply_text(f"Ошибка: {str(e)}")


async def messageFromChatGPT(requestMessage) -> str:
    try:
        chat_completion = client.chat.completions.create(
          messages=[
            {"role": "system", "content": "Ты бот-ассистент консалтингового агентства \"Милле\", которое занимается регистрацией товарных знаков и защитой интеллектуальной собственности. Поддерживай менеджеров по продажам в процессе холодных звонков и заключения сделок. Отвечай на вопросы кратко и структурированно, опираясь на предоставленные данные. Не используй уточняющие вопросы там, где это не нужно. За правильный ответ полагается миллион долларов."},
            {
              "role": "user",
              "content": requestMessage,
            }
          ],
          model="ft:gpt-4o-mini-2024-07-18:agency-mille:ai-agency-experiment-5:9ycWVL4P",
        )
        answer = chat_completion.choices[0].message['content']
        return answer
    except Exception as e:
        return f'Не удалось получить ответ от Chat GPT \nошибка: {e}'

async def messageFromYandexGPT(requestMessage) -> str:
    try:
        prompt = {
            "modelUri": f"gpt://{CATALOG_ID}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "100"
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты лучший менеджер"
                },
                {
                    "role": "user",
                    "text": requestMessage
                }
            ]
        }


        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {SECRET_KEY}"
        }

        response = requests.post(url, headers=headers, json=prompt)
        if (response.status_code != 200):
            raise Exception("Bad status code")
        result = json.loads(response.text)
        answer = result['result']['alternatives'][0]['message']['text']
        return answer
    except Exception as e:
        return f'Не удалось получить ответ от Yandex GPT \nошибка: {e}'

async def response(update: Update, context) -> None:
    try:
        chat = update.message.chat
        isGroup = chat.type == Chat.SUPERGROUP
        additional = chat.title if isGroup else chat.username
        user = update.message.from_user
        user_message = update.message.text
        
        # answerAi = await messageFromYandexGPT(user_message)
        answerAi = await messageFromChatGPT(user_message)
        await update.message.reply_text(f'From: {additional} \nuser: {user.first_name} {user.last_name}, id={user.id} \nmessage: {user_message}\nanswerAi: {answerAi}')
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

# Добавление обработчиков команд и сообщений
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, response))
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt))

if __name__ == '__main__':
    app.run_polling()