from download_data import start_downloading
from telebot import TeleBot, types
from dotenv import load_dotenv
import logging.config
import logging
import os


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('Running')

load_dotenv('.env')

bot_name: str = os.getenv('BOT_NAME')
token: str = os.getenv('BOT_TOKEN')
bot = TeleBot(token, threaded=True)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


@bot.message_handler()
def message_reply(msg: types.Message):
    global message
    message = msg
    text = message.text

    for country in the_world:
        if country == text:
            send_everything(country)


def send_everything(country):
    try:
        directory = f'static/{country}'

        for file in directory:
            path = directory + file
            print(path)

            if '.txt' in file:
                bot.send_message(message.chat.id, path)
            else:
                bot.send_photo(message.chat.id, path)

    except Exception:
        logging.error(f'Error occurred while trying to reach the {country} directory')


if __name__ == '__main__':
    with open('data/the-world.txt', 'r', encoding='utf-8') as the_world:
        the_world = [country.strip() for country in the_world.readlines()]

    bot.infinity_polling()
