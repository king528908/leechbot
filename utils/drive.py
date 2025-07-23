import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from config import GDRIVE_FOLDER_ID

def authenticate_drive():
    """Authenticate with Google Drive and return GoogleDrive object"""
    try:
        gauth = GoogleAuth()

        # Load saved credentials
        if os.path.exists("token.json"):
            gauth.LoadCredentialsFile("token.json")

        if gauth.credentials is None:
            if os.path.exists("credentials.json"):
                gauth.LocalWebserverAuth()
            else:
                raise FileNotFoundError("❌ credentials.json not found!")
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        # Save updated token
        gauth.SaveCredentialsFile("token.json")
        return GoogleDrive(gauth)

    except Exception as e:
        print(f"⚠️ Drive authentication error: {e}")
        raise e


def upload_file_to_drive(file_path):
    """Upload file to Google Drive and return shareable link"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    try:
        drive = authenticate_drive()
        file_name = os.path.basename(file_path)

        metadata = {'title': file_name}
        if GDRIVE_FOLDER_ID:
            metadata['parents'] = [{'id': GDRIVE_FOLDER_ID}]

        gfile = drive.CreateFile(metadata)
        gfile.SetContentFile(file_path)
        gfile.Upload()

        # Make file shareable
        gfile.InsertPermission({
            'type': 'anyone',
            'role': 'reader'
        })

        link = f"https://drive.google.com/file/d/{gfile['id']}/view"
        print(f"✅ Uploaded: {file_name} → {link}")
        return link

    except Exception as e:
        print(f"❌ Drive Upload Failed: {e}")
        raise Exception(f"Upload failed: {str(e)}")


def get_drive_usage():
    """Get Google Drive usage stats"""
    try:
        drive = authenticate_drive()
        about = drive.GetAbout()

        total = int(about['quotaBytesTotal'])
        used = int(about['quotaBytesUsed'])
        free = total - used
        percent = round((used / total) * 100, 2)

        return {
            'total': total,
            'used': used,
            'free': free,
            'percent_used': percent
        }

    except Exception as e:
        print(f"⚠️ Drive usage error: {e}")
        return None


def list_drive_files(limit=10):
    """List recent uploaded files from GDRIVE_FOLDER_ID"""
    try:
        drive = authenticate_drive()
        query = f"'{GDRIVE_FOLDER_ID}' in parents" if GDRIVE_FOLDER_ID else None

        file_list = drive.ListFile({
            'q': query,
            'maxResults': limit,
            'orderBy': 'createdDate desc'
        }).GetList()

        return [{
            'name': f['title'],
            'id': f['id'],
            'size': f.get('fileSize', 'Unknown'),
            'created': f['createdDate']
        } for f in file_list]

    except Exception as e:
        print(f"⚠️ Drive list error: {e}")
        return []
