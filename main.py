from download_data import start_downloading
from telebot import TeleBot
import logging

bot = TeleBot(token='12345')




if __name__ == '__main__':
    bot.infinity_polling()
