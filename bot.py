import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Загружаем API-ключи из .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Настраиваем API OpenAI
openai.api_key = OPENAI_API_KEY

# Функция обработки сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Получаем текст от пользователя
    
    try:
        # Отправляем запрос в ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150
        )
        
        # Отправляем ответ пользователю
        update.message.reply_text(response["choices"][0]["message"]["content"].strip())

    except Exception as e:
        update.message.reply_text("Ошибка при обращении к ChatGPT. Попробуйте позже.")

# Функция старта
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я бот ChatGPT. Задай мне вопрос.")

def main():
    # Создаем объект Updater
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    
    # Добавляем обработчики команд и сообщений
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
