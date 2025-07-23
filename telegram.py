# utils/telegram.py

import os
from telebot import TeleBot

def upload_to_telegram(bot: TeleBot, chat_id, file_path):
    filename = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        if filename.endswith(('.mp4', '.mkv', '.mov')):
            return bot.send_video(chat_id, f, caption=filename)
        elif filename.endswith(('.mp3', '.wav', '.flac')):
            return bot.send_audio(chat_id, f, caption=filename)
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return bot.send_photo(chat_id, f, caption=filename)
        else:
            return bot.send_document(chat_id, f, caption=filename)