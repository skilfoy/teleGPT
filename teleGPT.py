## teleGPT
## by Sean Kilfoy

import openai
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

messages = [
    {"role": "system", "content": "You're an AI assistant who is inspiring, helpful, creative, clever, and very friendly."}
]

# Set up the Telegram bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=messages[-1]['content'])

def reply(update, context):
    user_message = update.message.text
    messages.append({"role": "user", "content": user_message})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion.choices[0].message.content
    context.bot.send_message(chat_id=update.effective_chat.id, text=chat_response)

    messages.append({"role": "assistant", "content": chat_response})

# Set up the Telegram bot handlers
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
start_handler = MessageHandler(Filters.command & Filters.regex('^/start$'), start)
message_handler = MessageHandler(Filters.text & (~Filters.command), reply)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
