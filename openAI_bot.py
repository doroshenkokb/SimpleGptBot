import logging
import os
import sys

import openai
import telebot
from dotenv import load_dotenv

import message as msg

load_dotenv()

OPEN_AI_TOKEN = os.getenv('SECRET_API_KEY')
TG_TOKEN = os.getenv('SECRET_TG_TOKEN')


def check_tokens() -> bool:
    """Проверяет доступность переменных окружения."""
    env_variables = {
        'OPEN_AI_TOKEN': OPEN_AI_TOKEN,
        'TG_TOKEN': TG_TOKEN,
    }
    no_value = [
        var_name for var_name, value in env_variables.items() if not value
    ]
    if no_value:
        logging.critical(f'{msg.GLOBAL_VARIABLE_IS_MISSING} {no_value}')
        return False
    return True

bot = telebot.TeleBot(TG_TOKEN)
openai.api_key = OPEN_AI_TOKEN

@bot.message_handler(content_types=["text"])
def handle_text(message):
    """Отправка сообщения."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{message.text}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
    except Exception as e:
        bot.send_message(message.chat.id, "Какието траблы, введите тескт по новой")
        logging.error(f'Эррор: {e}') 
    bot.send_message(message.chat.id, response.choices[0].text)
    logging.info(f"Пользователь {message.from_user.username} отправил сообщение: {message.text}")
    logging.info(f"Бот отправил ответ: {response.choices[0].text}")


def main():
    """Основная логика работы бота."""
    if check_tokens():
        bot.polling()    
    else:
        sys.exit()

if __name__ == '__main__': 
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S',
        filename='bot_logs.log'
    )
    logger = logging.getLogger(__name__)
    logger.info('Бот стартует...')
    logger.info('Токены впорядке. Бот запущен...')
    main()
