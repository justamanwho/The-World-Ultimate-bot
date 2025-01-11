from telebot import TeleBot, types
from dotenv import load_dotenv
import logging
import os
from difflib import SequenceMatcher


load_dotenv('.env')
bot_name: str = os.getenv('BOT_NAME')
token: str = os.getenv('BOT_TOKEN')
bot = TeleBot(token, threaded=True)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

for handler in (logging.FileHandler(f'{logger.name}.log', encoding='utf-8'), logging.StreamHandler()):
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

file_objects = dict()


@bot.message_handler()
def message_reply(msg: types.Message):
    global message
    message = msg
    text = message.text

    for country in countries:
        if SequenceMatcher(None, country, text).ratio() > 0.7:
            filepaths = file_objects[country]
            for filename, file_object in filepaths.items():
                ext = filename.split('.')[-1].lower()

                send_by_name_ext(file_object, ext)
            break


def preload_files() -> None:

    directories = f'The-World\static'

    for directory in os.listdir(directories):
        dir_path = os.path.join(directories, directory)
        if os.path.isdir(dir_path):
            file_objects[directory] = {}  # Initialize once per directory

            for filename in os.listdir(dir_path):
                filepath = os.path.join(dir_path, filename)

                # Open the file in text or binary mode
                if filename.endswith('.txt'):
                    file_objects[directory][filename] = open(filepath, 'r', encoding='utf-8')

                elif filename.endswith('.png'):
                    file_objects[directory][filename] = open(filepath, 'rb')

            logger.info(f'Preloaded Directory {directory}')

    with open('start_message.txt', 'r') as readme:
        global start_message
        start_message = readme.read()


def close_files() -> None:
    for country in file_objects.values():
        for file_object in country.values():
            if file_object:
                file_object.close()
                logger.info(f"Closed File {file_object.name}")


def get_file_object(filename: str, filepath: str):
    file_object = file_objects.get(filename).get(filepath)

    return file_object


def send_by_name_ext(file_object, ext):
    try:
        file_object.seek(0)

        if ext == 'txt':
            bot.send_message(message.chat.id, file_object)
        else:
            bot.send_photo(message.chat.id, file_object)

        logger.info(f'File {file_object.name.split("/")[-1]} has been sent')
    except Exception as e:
        logger.error(f'Error while sending {file_object.name.split("/")[-1]} \n Traceback: {e}')


def send_start_message() -> None:
    bot.send_message(message.chat.id, start_message)
    logger.info(f'Start Message has been sent')


def error_handling() -> None:
    logger.info(f'Incorrect message: {message.text}')

    bot.reply_to(message, "Country doesn't exist", reply_markup=markup)
    img, ext = get_file_object('The World', 'The-World.png')

    send_by_name_ext(img, ext)


if __name__ == '__main__':
    preload_files()

    with open('The-World/the-world.txt', 'r', encoding='utf-8') as the_world:
        countries = [country.strip() for country in the_world.readlines()]
        print(countries)
        bot.infinity_polling()

    close_files()
