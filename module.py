from datetime import datetime 
import re 
from telegram import Update
from telegram.ext import CallbackContext
import logging 
from mnist.predict import make_predict 
from PIL import Image
import numpy as np 
import wget


def is_recent_message(prev, 
                      recent):

    if datetime.timestamp(recent) - datetime.timestamp(prev) < 20:
        return True
    else: 
        return False 

def start(update: Update, 
          context: CallbackContext):
    
    logging.info(f'Receiving message: {update.message}')
    
    if is_recent_message(update.message.date, datetime.now()):
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="I'm a bot, please talk to me!")
    
def user_id(update: Update, 
            context: CallbackContext):
    
    logging.info(f'Receiving message: {update.message}')
    
    if is_recent_message(update.message.date, datetime.now()):
        if update.message.chat.type == 'private':

            logging.info(f'Username: {update.message.from_user.first_name}(user_id: {update.message.from_user.id}) has requested a `user_id` service in private chat.')
            
            context.bot.send_message(chat_id=update.effective_chat.id, 
                                     text=f'Your user id is: {update.message.from_user.id}')
        
        else: 
            if update.message.reply_to_message is not None:
                
                logging.info(f'Username: {update.message.from_user.first_name}(user_id: {update.message.from_user.id}) has requested a `user_id` service in public chat. The target is {update.message.reply_to_message.from_user.first_name}(user_id: {update.message.reply_to_message.from_user.id})')
                
                context.bot.send_message(chat_id=update.effective_chat.id, 
                                         text=f'The user id of target is: {update.message.reply_to_message.from_user.id}')

            else: 
                
                logging.info(f'Username: {update.message.from_user.first_name} with id: {update.message.from_user.id} has requested a `user_id` service in prublic chat.')
                
                context.bot.send_message(chat_id=update.effective_chat.id, 
                                         text=f'Your user id is: {update.message.from_user.id}')

def predict(update: Update,
            context: CallbackContext):

    logging.info(f'Receiving predict request: {update.message}')

    if is_recent_message(update.message.date, datetime.now()):

        # Get file id from a list of image.
        for content in update.message.reply_to_message.photo[:1]:
            file_id = content.file_id

        # Get file URL using file id.
        file = context.bot.get_file(file_id)

        # Download file
        wget.download(file.file_path, out=f'/tmp/{file.file_unique_id}.jpg')

        # Load image and reshape/resize.
        image = Image.open(f'/tmp/{file.file_unique_id}.jpg')
        image = image.resize((28,28))
        image = np.array(image)[:, :, 0].flatten('F')[np.newaxis, :]

        # Pass the transformed image to the predict finction and get the prediction.
        prediction = make_predict(image)

        # Send the message back to the chat and announce the result.
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=open(f'/tmp/{file.file_unique_id}.jpg', 'rb'),
                               caption=f'The prediction of target image is {prediction}.',
                               timeout=30)

