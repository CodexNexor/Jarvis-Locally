import os
import time
import random
import requests
from dotenv import load_dotenv
from telethon.sync import TelegramClient
import TTS.tts  # Ensure this module is installed

# Load API credentials from .env
load_dotenv()
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = os.getenv("TELEGRAM_SESSION_PATH")

# Groq API Key (For AI Replies)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"  # Example model, change if needed

# Jarvis AI Role
JARVIS_ROLE = (
    "You are Jarvis, an AI assistant managing Telegram on behalf of Dheeraj. "
    "Dheeraj is currently busy, so you are responding to messages professionally and appropriately."
)

def get_unread_messages():
    """Fetch unread Telegram messages and return count and details."""
    with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        client.connect()
        if not client.is_user_authorized():
            print("[ERROR] Not logged in! Please log in first.")
            return 0, []

        unread_messages = []
        for dialog in client.iter_dialogs():
            if dialog.unread_count > 0:
                for message in client.iter_messages(dialog, limit=dialog.unread_count):
                    if not message.out:  # Only incoming messages
                        unread_messages.append((dialog.name, message.text))

        return len(unread_messages), unread_messages

def speak_unread_messages():
    """Announce unread messages using TTS."""
    unread_count, _ = get_unread_messages()

    if unread_count > 0:
        message = f"Sir,on my analysis there is {unread_count} unread Telegram messages. do you want me to reply"
    else:
        message = "No unread Telegram messages."

    TTS.tts.speak(message)  # Jarvis speaks

def generate_ai_reply(user_message):
    """Generate an AI-based reply using Groq API."""
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": JARVIS_ROLE},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": 100
        }

        response = requests.post(url, headers=headers, json=payload)
        response_json = response.json()

        return response_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

    except Exception as e:
        print(f"[ERROR] AI Reply Failed: {e}")
        return "Sorry, I couldn't generate a reply at the moment."

def handle_telegram_messages():
    """Check messages & reply if user is busy."""
    unread_count, unread_messages = get_unread_messages()

    if unread_count == 0:
        print("[INFO] No unread messages.")
        return

    print(f"[INFO] Processing {unread_count} unread messages...")

    with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        for chat_name, message_text in unread_messages:
            print(f"[NEW MESSAGE] From {chat_name}: {message_text}")

            ai_reply = generate_ai_reply(message_text)
            if ai_reply:
                time.sleep(random.uniform(1, 3))  # Simulate human-like delay
                client.send_message(chat_name, ai_reply)
                print(f"[AUTO-REPLY] Sent to {chat_name}: {ai_reply}")

def execute_task():
    """Main function for automation.py to trigger Telegram checking and AI replies."""
    speak_unread_messages()
    handle_telegram_messages()
