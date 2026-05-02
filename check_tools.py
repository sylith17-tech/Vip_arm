import subprocess
import os

def check_system():
    tools = ['yt-dlp', 'ffmpeg', 'ffprobe']
    print("--- VIP_ARM OS Diagnostic Status ---")
    for tool in tools:
        try:
            res = subprocess.run([tool, '--version'], capture_output=True)
            print(f"[✅] {tool}: Version detected")
        except FileNotFoundError:
            print(f"[❌] {tool}: NOT FOUND (أداة مفقودة)")

    # فحص صلاحيات مجلد التحميل
    download_path = "downloads" # غيره للمجلد الذي تستخدمه
    if os.path.exists(download_path):
        print(f"[✅] Directory '{download_path}' exists.")
        if os.access(download_path, os.W_OK):
            print(f"[✅] Write permissions: OK")
        else:
            print(f"[❌] Write permissions: DENIED")
    else:
        print(f"[❌] Directory '{download_path}' is missing.")

check_system()
