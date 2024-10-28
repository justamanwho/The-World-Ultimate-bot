from download_data import start_downloading
from typing import IO
from telebot import TeleBot, types
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
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


file_objects = dict()


@bot.message_handler()
def message_reply(msg: types.Message):
    global message
    message = msg
    text = message.text

    # for country in the_world:
    #     # add regex or better use comparing tool and make like 90% purity or some shit
    #     if country == text:
    #
    #         filepaths = file_objects[country]
    #         for filepath in filepaths:
    #             file_object, ext = get_file_object(country, filepath)
    #
    #             send_by_name_ext(file_object, ext)

    filepaths = file_objects['Afghanistan']
    print(filepaths)
    for filename, file_object in filepaths.items():
        ext = filename.split('.')[-1].lower()

        send_by_name_ext(file_object, ext=ext)


def preload_files() -> None:

    directories = f'static'

    for directory in os.listdir(directories):
        dir_path = os.path.join(directories, directory)
        if os.path.isdir(dir_path):
            file_objects[directory] = {}  # Initialize once per directory

            for filename in os.listdir(dir_path):
                filepath = os.path.join(dir_path, filename)

                # Open the file in text or binary mode
                if filename.endswith('.txt'):
                    file_objects[directory][filename] = open(filepath, 'r', encoding='utf-8')
                else:
                    file_objects[directory][filename] = open(filepath, 'rb')

            logger.info(f'Preloaded Directory {directory}')

    with open('data/start_message.txt', 'r') as readme:
        global start_message
        start_message = readme.read()


def close_files() -> None:
    for country in file_objects.values():
        for file_object in country.values():
            if file_object:
                file_object.close()
                logger.info(f"Closed File {file_object.name}")


# def find_everything(country):
#     try:
#         directory = f'static\{country}'
#         country_file_paths = []
#
#         for filename in os.listdir(directory):
#             filepath = os.path.join(directory, filename)
#
#             country_file_paths.append(filepath)
#
#         return country_file_paths
#
#     except Exception:
#         logging.error(f'Error occurred while trying to reach the {country} directory')


def get_file_object(filename: str, filepath: str):

    file_object = file_objects.get(filename).get(filepath)

    return file_object


def send_by_name_ext(file_object, ext):
    try:
        if ext == 'txt':
            bot.send_message(message.chat.id, file_object)
        elif ext == 'svg':
            # change it to photo somehow
            bot.send_document(message.chat.id, file_object)
        else:
            file_object.seek(0)

            image = Image.open(file_object)

            ext = 'jpeg' if ext in ['jpg', 'jfif'] else ext
            image = image.convert('RGB') if image.mode == 'RGBA' else image

            image_data = BytesIO()
            image.save(image_data, format=ext.upper())
            image_data.seek(0)

            bot.send_photo(message.chat.id, image)

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

    with open('data/the-world.txt', 'r', encoding='utf-8') as the_world:
        the_world = [country.strip() for country in the_world.readlines()]
        bot.infinity_polling()

    close_files()
