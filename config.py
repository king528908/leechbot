import os

# --- Bot Configuration ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))  # Replace with your Telegram user ID

# --- Upload Configuration ---
UPLOAD_MODE = os.getenv("UPLOAD_MODE", "telegram").lower()  # "telegram" or "drive"

# --- Google Drive Folder ID ---
GDRIVE_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID", "")  # Leave blank for root

# --- Download Settings ---
MAX_FILE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB size limit for downloads
DOWNLOAD_TIMEOUT = 300  # Timeout for download requests (in seconds)

# --- Allowed File Extensions ---
ALLOWED_EXTENSIONS = [
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm',
    '.mp3', '.wav', '.flac', '.aac', '.ogg',
    '.zip', '.rar', '.7z', '.tar', '.gz',
    '.pdf', '.doc', '.docx', '.txt',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp'
]

# --- Status Messages ---
STATUS_MESSAGES = {
    'starting': '🔄 Starting download...',
    'downloading': '⬇️ Downloading...',
    'uploading': '⬆️ Uploading...',
    'completed': '✅ Completed!',
    'failed': '❌ Failed!',
    'cancelled': '⏹️ Cancelled!'
}