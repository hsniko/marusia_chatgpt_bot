import os
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Получение API-ключей из переменных окружения
openai.api_key = os.getenv("OPENAI_API_KEY")  # Замените переменную окружения на вашу (не храните ключ в коде)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Замените переменную окружения на вашу (не храните токен в коде)

# Проверка на наличие ключей в переменных окружения
if not openai.api_key or not TELEGRAM_TOKEN:
    raise ValueError("Не заданы необходимые переменные окружения: OPENAI_API_KEY и TELEGRAM_TOKEN")

# Функция обработки сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Получаем сообщение пользователя
    
    try:
        # Запрос к OpenAI ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=[{"role": "user", "content": user_message}]
        )
        # Отправляем ответ обратно пользователю
        update.message.reply_text(response["choices"][0]["message"]["content"])
    
    except openai.error.OpenAIError as e:
        update.message.reply_text(f"Произошла ошибка при взаимодействии с OpenAI: {e}")
    except Exception as e:
        update.message.reply_text(f"Произошла ошибка: {e}")

# Функция старта
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот ChatGPT для Маруси. Задайте вопрос.')

def main():
    # Инициализация бота
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    # Добавление обработчиков команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
