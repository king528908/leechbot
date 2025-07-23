# handlers/leech.py

import os
import time
import subprocess
from telebot.types import Message
from config import upload_mode, MAX_FILE_SIZE, STATUS_MESSAGES
from utils.drive import upload_file_to_drive
from utils.telegram import upload_to_telegram  # You can define this separately

def leech_command(bot, message: Message, url: str):
    chat_id = message.chat.id
    msg = bot.reply_to(message, STATUS_MESSAGES['starting'])

    try:
        file_name = f"downloads/{int(time.time())}.mp4"
        cmd = ["yt-dlp", "-o", file_name, url]
        bot.edit_message_text(STATUS_MESSAGES['downloading'], chat_id=chat_id, message_id=msg.message_id)

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception("Download failed")

        downloaded_file = get_downloaded_file(file_name)

        if os.path.getsize(downloaded_file) > MAX_FILE_SIZE:
            raise Exception("❌ File too large for Telegram (2GB limit)")

        bot.edit_message_text(STATUS_MESSAGES['uploading'], chat_id=chat_id, message_id=msg.message_id)

        if upload_mode == "telegram":
            sent = upload_to_telegram(bot, chat_id, downloaded_file)
            bot.edit_message_text(STATUS_MESSAGES['completed'], chat_id=chat_id, message_id=msg.message_id)
        elif upload_mode == "drive":
            link = upload_file_to_drive(downloaded_file)
            bot.edit_message_text(f"✅ Uploaded to Drive:\n{link}", chat_id=chat_id, message_id=msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"{STATUS_MESSAGES['failed']}\n\n{str(e)}", chat_id=chat_id, message_id=msg.message_id)

    finally:
        # Clean up file
        try:
            if os.path.exists(file_name):
                os.remove(file_name)
        except:
            pass

def get_downloaded_file(pattern):
    # yt-dlp may create different file names
    if os.path.isfile(pattern):
        return pattern
    for f in os.listdir("downloads"):
        if f.endswith(".mp4"):
            return os.path.join("downloads", f)
    raise FileNotFoundError("File not found after download")