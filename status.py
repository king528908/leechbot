# status.py
import time

def format_status(filename, percent, downloaded, speed, eta, engine, user_id, upload_mode):
    """Format download status message"""
    status = f"""
⬇️ Downloading with {engine.upper()}

📁 File: {filename}
👤 User: {user_id}
📊 Progress: {percent}
📦 Downloaded: {downloaded}
🚀 Speed: {speed}
⏰ ETA: {eta}
📤 Upload Mode: {upload_mode.upper()}

Use /status to see all downloads
"""
    return status.strip()


def format_global_status(active_downloads, start_time, download_stats=None):
    """Enhanced global status with statistics"""
    if not active_downloads:
        uptime = int(time.time() - start_time)
        success_rate = (download_stats['success'] / (download_stats['total'] + 1) * 100) if download_stats else 0
        return f"""
📊 Jarvis Leech Bot v3.1 - TURBO STATUS

📥 Active Downloads: `0`
🕒 Uptime: `{format_time(uptime)}`
📈 Success Rate: `{success_rate:.1f}%`
🟢 Status: `TURBO MODE READY` 🚀

🚀 TURBO Features:
✅ Multi-threaded downloads (up to 8x faster)
✅ Real-time progress tracking
✅ Smart resume capability
✅ Advanced retry logic

📊 Session Stats:
• Total Downloads: `{download_stats['total'] if download_stats else 0}`
• Successful: `{download_stats['success'] if download_stats else 0}` ✅
• Failed: `{download_stats['failed'] if download_stats else 0}` ❌

Use `/turbo [url]` for maximum speed!
""".strip()

    status_text = "🚀 **TURBO DOWNLOADS - LIVE STATUS**\n\n"
    turbo_count = 0
    regular_count = 0

    for fid, data in active_downloads.items():
        elapsed = int(time.time() - data['start'])
        filename = data.get('filename', 'Unknown')
        status = data.get('status', 'Unknown')
        user = data.get('user', 'Unknown')
        quality = data.get('quality', 'Unknown')
        format_type = data.get('format', 'Unknown')
        is_turbo = data.get('is_turbo', False)
        speed = data.get('speed', '0 MB/s')
        progress = data.get('progress', '0%')
        eta = data.get('eta', 'Unknown')
        threads = data.get('threads', 1)

        icon = "🚀" if is_turbo else "📥"
        if is_turbo:
            turbo_count += 1
        else:
            regular_count += 1

        progress_bar = create_progress_bar(progress)

        status_text += f"{icon} **{filename[:30]}{'...' if len(filename) > 30 else ''}**\n"
        status_text += f"├─ 👤 User: `{user}` | ⚡ Threads: `{threads}`\n"
        status_text += f"├─ 📊 {progress_bar}\n"
        status_text += f"├─ 🚀 Speed: `{speed}` | ⏰ ETA: `{eta}`\n"
        status_text += f"├─ 🎯 `{quality}` | 📁 `{format_type}` | ⏱️ `{format_time(elapsed)}`\n"
        status_text += f"└─ 📊 Status: `{status}`\n\n"

    uptime = int(time.time() - start_time)
    success_rate = (download_stats['success'] / (download_stats['total'] + 1) * 100) if download_stats else 0

    status_text += f"""
📈 **PERFORMANCE SUMMARY**
🚀 Turbo: `{turbo_count}` | 📥 Regular: `{regular_count}` | 📊 Success: `{success_rate:.1f}%`
🕒 Uptime: `{format_time(uptime)}` | 📊 Total: `{download_stats['total'] if download_stats else 0}`

*Updates every 3 seconds • Use /detailed for more info*
"""
    return status_text.strip()


def create_progress_bar(progress_str, length=15):
    """Create a visual progress bar"""
    try:
        progress = float(progress_str.replace('%', ''))
        filled = int((progress / 100) * length)
        empty = length - filled
        bar = '█' * filled + '░' * empty
        return f"`{bar}` {progress:.1f}%"
    except:
        return f"`{'░' * length}` 0%"


def format_time(seconds):
    """Format seconds into human readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"