# -*- coding: utf-8 -*-

import os
import urllib.request

home_dir = os.path.expanduser("~")
target_dir = os.path.join(home_dir, "Applications", "cursor")

os.makedirs(target_dir, exist_ok=True)

url = "https://downloader.cursor.sh/linux/appImage/x64"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

existing_files = [f for f in os.listdir(target_dir) if f.endswith('.AppImage')]
if existing_files:
    print("Cursor Checking for updates to...")
else:
    print("Cursor Installing...")
    
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        new_filename = response.info().get_filename() or "cursor.AppImage"
        new_version = new_filename.split('-')[1] if '-' in new_filename else None
        
        existing_files = [f for f in os.listdir(target_dir) if f.endswith('.AppImage')]
        if existing_files:
            existing_version = existing_files[0].split('-')[1] if '-' in existing_files[0] else None
            
            if new_version and existing_version and new_version == existing_version:
                print(f"Already the latest version{existing_version}for the following applications. No download is required.")
                exit()

        print("New version detected. Downloading...")
        file_size = int(response.info().get('Content-Length', -1))
        downloaded = 0
        block_size = 8192
        target_path = os.path.join(target_dir, new_filename)
        with open(target_path, 'wb') as out_file:
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                downloaded += len(buffer)
                out_file.write(buffer)
                if file_size > 0:
                    percent = downloaded * 100 / file_size
                    print(f"\rDownload Progress: {percent:.2f}%", end='', flush=True)
        print("\nダウンロード完了!")
        print(f"Cursor AppImageThe new version of the software has been successfully downloaded!: {target_path}")
        
        old_files = [f for f in os.listdir(target_dir) if f.endswith('.AppImage') and f != new_filename]
        for old_file in old_files:
            old_file_path = os.path.join(target_dir, old_file)
            try:
                os.remove(old_file_path)
                print(f"Removed old version: {old_file}")
            except Exception as e:
                print(f"Older versions{old_file}An error occurred while deleting the: {str(e)}")
        
        os.chmod(target_path, 0o755) 
        print("Cursor AppImage has been successfully downloaded and set to run.")

        symlink_path = os.path.join(target_dir, "cursor.AppImage")
        if os.path.exists(symlink_path):
            os.remove(symlink_path)
        os.symlink(target_path, symlink_path)
        print(f"Symbolic links have been updated.: {symlink_path}")

        icon_path = os.path.expanduser("~/.local/share/icons/cursor-icon.svg")
        if not os.path.exists(icon_path):
            os.makedirs(os.path.dirname(icon_path), exist_ok=True)
            icon_url = "https://www.cursor.so/brand/icon.svg"
            urllib.request.urlretrieve(icon_url, icon_path)
            print(f"Icons downloaded: {icon_path}")

        desktop_file_path = os.path.expanduser("~/.local/share/applications/cursor.desktop")
        desktop_content = f"""[Desktop Entry]
Name=Cursor
Exec={symlink_path}
Terminal=false
Type=Application
Icon={icon_path}
StartupWMClass=Cursor
X-AppImage-Version=latest
Comment=Cursoris an AI-first coding environment.
MimeType=x-scheme-handler/cursor;
Categories=Utility;Development
"""
        with open(desktop_file_path, 'w') as f:
            f.write(desktop_content)
        os.chmod(desktop_file_path, 0o755)
        print(f".desktop File has been updated.: {desktop_file_path}")
        
        desktop_symlink_path = os.path.join(target_dir, "cursor.desktop")
        if os.path.exists(desktop_symlink_path):
            os.remove(desktop_symlink_path)
        os.symlink(desktop_file_path, desktop_symlink_path)
        
except urllib.error.HTTPError as e:
    print(f"Download failed: HTTPエラー {e.code}")
except urllib.error.URLError as e:
    print(f"Download failed: URLエラー {e.reason}")
except Exception as e:
    print(f"Download failed.: {str(e)}")
