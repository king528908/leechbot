# handlers/mirror.py

import os
import time
import subprocess
from utils.telegram import upload_to_telegram
from utils.drive import upload_file_to_drive
from config import upload_mode, MAX_FILE_SIZE, STATUS_MESSAGES

def mirror_handler(bot, message, url):
    chat_id = message.chat.id
    msg = bot.reply_to(message, STATUS_MESSAGES['starting'])

    try:
        timestamp = int(time.time())
        output = f"downloads/{timestamp}_%(title)s.%(ext)s"
        cmd = ["yt-dlp", "-o", output, url]

        bot.edit_message_text(STATUS_MESSAGES['downloading'], chat_id=chat_id, message_id=msg.message_id)
        subprocess.run(cmd, check=True)

        downloaded_file = get_latest_file("downloads/")
        if not downloaded_file or not os.path.exists(downloaded_file):
            raise Exception("❌ File download failed!")

        if os.path.getsize(downloaded_file) > MAX_FILE_SIZE:
            raise Exception("❌ File too large for Telegram")

        bot.edit_message_text(STATUS_MESSAGES['uploading'], chat_id=chat_id, message_id=msg.message_id)

        if upload_mode == "telegram":
            upload_to_telegram(bot, chat_id, downloaded_file)
            bot.edit_message_text(STATUS_MESSAGES['completed'], chat_id=chat_id, message_id=msg.message_id)
        else:
            drive_link = upload_file_to_drive(downloaded_file)
            bot.edit_message_text(f"✅ Uploaded to Drive:\n{drive_link}", chat_id=chat_id, message_id=msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"{STATUS_MESSAGES['failed']}\n\n{str(e)}", chat_id=chat_id, message_id=msg.message_id)

    finally:
        try:
            if downloaded_file and os.path.exists(downloaded_file):
                os.remove(downloaded_file)
        except:
            pass

def get_latest_file(folder):
    files = sorted(
        [os.path.join(folder, f) for f in os.listdir(folder)],
        key=os.path.getmtime,
        reverse=True
    )
    return files[0] if files else None