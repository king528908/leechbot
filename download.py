# handlers/download.py

import os
import time
import subprocess
from telebot import types
from config import upload_mode, ALLOWED_EXTENSIONS
from utils.drive import upload_file_to_drive

def run_download(url, message, bot):
    msg = bot.send_message(message.chat.id, "🔄 Download starting...")

    try:
        output_template = f"downloads/{int(time.time())}_%(title).100s.%(ext)s"
        os.makedirs("downloads", exist_ok=True)

        command = [
            "yt-dlp",
            "-o", output_template,
            "--no-playlist",
            "--newline",
            url
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        filename = None

        for line in process.stdout:
            if "[download] Destination: " in line:
                filename = line.strip().split("Destination: ")[1]
                bot.edit_message_text(f"📥 Downloading...\n\n`{os.path.basename(filename)}`", chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")
            elif "%" in line:
                bot.edit_message_text(f"⬇️ {line.strip()}", chat_id=message.chat.id, message_id=msg.message_id)

        process.wait()

        if process.returncode != 0 or not filename or not os.path.exists(filename):
            bot.edit_message_text("❌ Download failed.", chat_id=message.chat.id, message_id=msg.message_id)
            return

        bot.edit_message_text("✅ Download complete. Uploading...", chat_id=message.chat.id, message_id=msg.message_id)

        if upload_mode == "drive":
            link = upload_file_to_drive(filename)
            bot.send_message(message.chat.id, f"✅ Uploaded to Google Drive:\n{link}")
        else:
            with open(filename, "rb") as f:
                bot.send_document(message.chat.id, f)

        os.remove(filename)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {e}")