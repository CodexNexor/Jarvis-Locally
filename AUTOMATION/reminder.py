import json
import os
import datetime
import threading
import time
import TTS.tts as tts  # Import your TTS module

REMINDER_FILE = "C:\\Users\\DHEERAJ\\Desktop\\jarvis\\Assists\\reminders.json"

def load_reminders():
    """Load reminders from JSON file."""
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_reminders(reminders):
    """Save reminders to JSON file."""
    with open(REMINDER_FILE, "w") as file:
        json.dump(reminders, file, indent=4)

def execute_task(time=None, message=None, description=None):
    """Sets a reminder with a description and saves it."""
    if time and message:
        try:
            # Validate and format the time
            reminder_time = datetime.datetime.strptime(time, "%H:%M").time()
            reminder = {
                "time": time,
                "message": message,
                "description": description or "No description provided"
            }

            # Load existing reminders, add new one, and save
            reminders = load_reminders()
            reminders.append(reminder)
            save_reminders(reminders)

            print(f"[INFO] Reminder set for {time}: {message} - {description}")

        except ValueError:
            print("[ERROR] Invalid time format. Use HH:MM (24-hour format).")
    else:
        print("[ERROR] Missing reminder parameters.")

def check_reminders():
    """Continuously checks for due reminders and announces them via TTS."""
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        reminders = load_reminders()
        updated_reminders = []

        for reminder in reminders:
            if reminder["time"] == now:
                announcement = f"Sir, I think it's time for {reminder['message']}. {reminder['description']}."
                print(f"[ALERT] {announcement}")  # Debugging
                tts.speak(announcement)  # Send reminder to TTS for speaking

            else:
                updated_reminders.append(reminder)

        save_reminders(updated_reminders)
        time.sleep(60)  # Check every 60 seconds

# Start reminder checking in a separate thread
threading.Thread(target=check_reminders, daemon=True).start()

# Example usage:
if __name__ == "__main__":
    execute_task("09:00", "Meeting", "Discuss project progress with the team.")
