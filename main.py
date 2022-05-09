from telegram.ext import Updater
import logging 
from datetime import datetime 
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import MessageHandler, Filters
import re 
import configparser
from module import start 
from module import search_content
from module import user_id
from module import predict

import sys 


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['TG_BOT_TOKEN']['TOKEN']

    updater = Updater(token=token, 
                  use_context=True)

    dispatcher = updater.dispatcher
    
    logging.basicConfig(filename='kurisu-amadeus-bot.log', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

    start_handler = CommandHandler('start', start)
    uid_handler = CommandHandler('userid', user_id)
    predict_handler = CommandHandler('predict', predict)

    
    # Add Commandline handler
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(uid_handler)
    dispatcher.add_handler(predict_handler)
    
    
    # Note: The order of adding handlers is important.
    # If adding a CommandHandler after a set of MessageHandler, the last CommandHandler will not works.

    try:
        updater.start_polling()
    except KeyboardInterrupt:
        updater.stop()
        sys.exit(0)

if __name__ == '__main__':
    main()
