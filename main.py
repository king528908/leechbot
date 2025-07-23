import os
import time
import subprocess
from telebot import TeleBot, types
from config import BOT_TOKEN, OWNER_ID, UPLOAD_MODE
from utils.drive import upload_file_to_drive

# Bot setup
bot = TeleBot(BOT_TOKEN)
start_time = time.time()

# ---------- Start ----------
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📥 Download", callback_data="help_download"),
        types.InlineKeyboardButton("⚙️ Settings", callback_data="help_settings")
    )
    markup.add(
        types.InlineKeyboardButton("📊 Status", callback_data="show_status"),
        types.InlineKeyboardButton("📈 Stats", callback_data="show_stats")
    )
    markup.add(types.InlineKeyboardButton("ℹ️ About", callback_data="show_about"))

    welcome = f"""
🤖 Welcome to Jarvis Leech Bot v3.1 - TURBO

🚀 Features:
• Multi-threaded downloads (5x speed)
• Upload to Telegram or Drive

📤 Upload Mode: `{UPLOAD_MODE.upper()}`
👑 Owner: `{OWNER_ID}`
"""
    bot.reply_to(message, welcome, parse_mode="Markdown", reply_markup=markup)

# ---------- Callback ----------
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    if data == "help_download":
        bot.edit_message_text("Use /leech [url] or /ytdl [url] to start downloading.", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif data == "help_settings":
        bot.edit_message_text("/setmode [telegram/drive] — Upload mode\n/setquality — Video quality", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif data == "show_status":
        uptime = int(time.time() - start_time)
        bot.edit_message_text(f"🕒 Uptime: {uptime}s\n🔄 Bot is running smoothly.", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
    elif data == "show_stats":
        bot.edit_message_text("📊 Stats: Downloads completed, success rate, etc.", chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif data == "show_about":
        bot.edit_message_text(f"ℹ️ Jarvis Leech Bot by Jarvis AI\nMode: {UPLOAD_MODE}", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")

# ---------- /ping ----------
@bot.message_handler(commands=["ping"])
def ping(message):
    start_ping = time.time()
    msg = bot.reply_to(message, "🏓 Pinging...")
    latency = round((time.time() - start_ping) * 1000, 2)
    bot.edit_message_text(f"🏓 Pong! `{latency} ms` ⚡", chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")

# ---------- Download Handler ----------
@bot.message_handler(commands=["leech", "mirror", "ytdl", "video", "turbo", "mp3"])
def handle_download(message):
    try:
        url = message.text.split(" ", 1)[1].strip()
        msg = bot.reply_to(message, "🔄 Starting download...")

        output_template = f"downloads/{int(time.time())}_%(title).80s.%(ext)s"
        os.makedirs("downloads", exist_ok=True)

        command = [
            "yt-dlp",
            "-o", output_template,
            "--no-playlist",
            url
        ]

        if message.text.startswith("/mp3"):
            command += ["--extract-audio", "--audio-format", "mp3"]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        filename = None

        for line in process.stdout:
            if "Destination:" in line:
                filename = line.strip().split("Destination: ")[-1]
                bot.edit_message_text(f"📄 `{os.path.basename(filename)}`\n⬇️ Downloading...", chat_id=message.chat.id, message_id=msg.message_id, parse_mode="Markdown")

        process.wait()

        if process.returncode != 0 or not filename or not os.path.exists(filename):
            bot.edit_message_text("❌ Download failed.", chat_id=message.chat.id, message_id=msg.message_id)
            return

        bot.edit_message_text("✅ Download complete. Uploading...", chat_id=message.chat.id, message_id=msg.message_id)

        if UPLOAD_MODE == "drive":
            link = upload_file_to_drive(filename)
            bot.send_message(message.chat.id, f"✅ Uploaded to Drive:\n{link}")
        else:
            with open(filename, "rb") as f:
                bot.send_document(message.chat.id, f)

        os.remove(filename)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {e}")

# ---------- Start Polling ----------
print("🚀 Bot is running...")
bot.infinity_polling()