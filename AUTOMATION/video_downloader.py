import os
import yt_dlp
import pygetwindow as gw
import pyperclip
import time
import pyautogui
import subprocess
from TTS.tts import speak  # Assuming you have a `speak` function in your TTS system

def get_current_tab_url():
    """Extracts the URL from the active browser tab."""
    browser_windows = [win for win in gw.getAllWindows() if "Google Chrome" in win.title or "Brave" in win.title]
    if browser_windows:
        window = browser_windows[0]
        window.activate()
        time.sleep(1)  # Allow time for activation
        pyperclip.copy('')  # Clear clipboard
        pyautogui.hotkey('ctrl', 'l')  # Focus address bar
        pyautogui.hotkey('ctrl', 'c')  # Copy URL
        time.sleep(1)  # Allow clipboard to update
        return pyperclip.paste()
    return None

def download_video(url, play_after_download=False):
    """Downloads the video at 720p quality and optionally plays it after saving."""
    if not url:
        print("[ERROR] No valid URL provided for video download.")
        return

    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    ydl_opts = {
        'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = os.path.join(download_folder, f"{info['title']}.mp4")

        print(f"Download complete: {file_path}")  # Notify user after download completion

        # Notify the user with TTS
        speak("SORRY Sir To disturb you but, your video has been downloaded successfully.")  # Call your TTS system here

        if play_after_download:
            # For Windows
            if os.name == 'nt':
                subprocess.run(["start", "", file_path], shell=True)
            # For macOS
            elif os.name == 'posix':
                subprocess.run(["open", file_path])
            # For Linux
            elif os.name == 'posix':
                subprocess.run(["xdg-open", file_path])

    except Exception as e:
        print(f"[ERROR] Failed to download video: {e}")
        # Notify the user if there was an error
        speak("Sorry, I couldn't download the video.")  # TTS for error
