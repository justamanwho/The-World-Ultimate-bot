from telebot import TeleBot, types
from dotenv import load_dotenv
from fuzzywuzzy import fuzz
import logging
import json
import os


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

    key_start_words = ['start', 'help', 'instructions', '/start', '/help', '/instructions']
    if text in key_start_words:
        send_start_message()
    if text == 'The World':
        send_by_name_ext(file_objects['The World'], 'png')
    else:
        country = find_country_name(text)
        if country:
            send_country_data(country)
        else:
            error_handling()


def find_country_name(text):
    text = text.upper()
    best_match = ''
    highest_similarity = 0

    for key, values in countries.items():
        aliases = [key.upper()]
        aliases.extend([value.upper() for value in values])

        for alias in aliases:
            try:
                similarity = fuzz.ratio(text, alias)

                # Update best match if the similarity is higher than the previous highest
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match = key

            except (TypeError, ValueError) as e:
                logger.error(f"Error comparing '{text}' with '{alias}': {e}")
                continue

    if best_match and highest_similarity > 65:
        logger.info(f'Matched {text} with {best_match} by {highest_similarity} similarity')

        return file_objects.get(best_match, None)
    else:
        logger.info(f'Similarity of {text} with {best_match} was too low: {highest_similarity}')

        return None


def send_country_data(data):
    files_needed = ['The_Coat_of_Arms.png', 'The_Flag.png', 'The_Map.png', 'The_Seal.png',
                    'Capital.txt', 'Summary.txt', 'Area.txt', 'Population.txt', 'GDP.txt', 'Currency.txt']

    for file_path in files_needed:
        ext = file_path.split('.')[-1].lower()

        try:
            file_object = data[file_path]
            send_by_name_ext(file_object, ext)
        except KeyError:
            pass


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

    # The Map of The World
    file_objects['The World'] = open('The-World-Map.png', 'rb')

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
    send_by_name_ext(file_objects['The World'], 'png')
    bot.reply_to(message, 'Not found. Please, try to type in an official name\nor alpha2/alpha3 code such as LU/LUX', reply_markup=markup)

    logger.info(f'Incorrect message: {message.text}')


if __name__ == '__main__':
    preload_files()

    with open('Countries-Aliases/aliases.json', 'r', encoding='utf-8') as json_file:
        countries = json.load(json_file)

        bot.infinity_polling()

    close_files()
