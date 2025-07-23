import os
from pydrive.auth import GoogleAuth

def generate_drive_token():
    """Generate and save Google Drive OAuth2 token"""
    try:
        # Check for credentials.json file
        if not os.path.exists('credentials.json'):
            print("❌ [ERROR] credentials.json not found!")
            print("📋 Please follow these steps to set up Google Drive API:")
            print("1️⃣ Visit: https://console.developers.google.com/")
            print("2️⃣ Create or select a project")
            print("3️⃣ Enable Google Drive API")
            print("4️⃣ Create OAuth2.0 credentials (Desktop App)")
            print("5️⃣ Download and rename as 'credentials.json'")
            return False

        # Initialize PyDrive Auth
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Opens browser for authentication
        
        # Save the generated token
        gauth.SaveCredentialsFile("token.json")
        
        print("✅ Authentication successful!")
        print("🔐 token.json saved.")
        return True

    except Exception as e:
        print(f"❌ [FAILED] Google Drive Authentication Error:\n{str(e)}")
        return False

if __name__ == "__main__":
    print("🔐 Google Drive Authentication Setup")
    print("=" * 40)
    generate_drive_token()