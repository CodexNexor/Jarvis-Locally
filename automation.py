import os
import json
import groq
import subprocess
import time

import AUTOMATION.youtube_song as youtube_song
import AUTOMATION.email_checker as email_checker
import AUTOMATION.telegram_checker as telegram_checker
import AUTOMATION.reminder as reminder
import AUTOMATION.open as open_app
import AUTOMATION.video_downloader as video_downloader
import AUTOMATION.image_gen as image_gen
import AUTOMATION.vision as vision

import TTS.tts
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configure Groq AI client
client = groq.Client(api_key=GROQ_API_KEY)

# Store subprocess for controller
control_process = None

# Task mapping
AUTOMATION_TASKS = {
    "play_music": youtube_song.execute_task,
    "check_email": email_checker.execute_task,
    "check_telegram": telegram_checker.execute_task,
    "set_reminder": reminder.execute_task,
    "open_application": open_app.execute_task,
    "download_video": video_downloader.download_video,
    "generate_image": image_gen.generate_image,
    "vision": vision.execute_task
}

# Updated AI role with clear vision command detection
AUTOMATION_ROLE = (
    "You are an advanced task separator AI system for a voice assistant named Jarvis.\n"
    "Your job is to analyze the user query and select the correct automation module to execute.\n"
    "Always return valid JSON in this exact format:\n\n"

    "Example Outputs:\n"
    "{ \"action\": \"play_music\", \"parameters\": { \"song\": \"song name\" } }\n"
    "{ \"action\": \"check_email\", \"parameters\": {} }\n"
    "{ \"action\": \"check_telegram\", \"parameters\": {} }\n"
    "{ \"action\": \"set_reminder\", \"parameters\": { \"time\": \"HH:MM\", \"message\": \"reminder text\" } }\n"
    "{ \"action\": \"control_pc\", \"parameters\": {} }\n"
    "{ \"action\": \"stop_control_pc\", \"parameters\": {} }\n"
    "{ \"action\": \"open_application\", \"parameters\": { \"name\": \"Chrome\" } }\n"
    "{ \"action\": \"download_video\", \"parameters\": { \"url\": \"video url\", \"play_after\": true } }\n"
    "{ \"action\": \"generate_image\", \"parameters\": { \"description\": \"image of a robot in space\" } }\n"
    "{ \"action\": \"vision\", \"parameters\": {} }\n\n"

    "Special Rules:\n"
    "- If the user says things like 'what is this', 'look at this', 'what do you see', 'describe this', 'use your camera' — treat it as a vision task → action = vision\n"
    "- If it's about emails or Gmail, use 'check_email'.\n"
    "- If it's about messages, use 'check_telegram'.\n"
    "- If it's about listening to music or YouTube, use 'play_music'.\n"
    "- If it's visual analysis, use 'vision'.\n"
    "- Do not return extra text, just pure JSON response.\n"
)

def classify_and_route_task(user_query):
    """Uses Groq AI to classify and route automation tasks."""
    try:
        print(f"[DEBUG] Received query in automation.py: {user_query}")

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": AUTOMATION_ROLE},
                {"role": "user", "content": user_query}
            ],
            response_format={"type": "json_object"}
        )

        if response and response.choices:
            task_data = response.choices[0].message.content
            print(f"[DEBUG] AI Response from Groq: {task_data}")

            if isinstance(task_data, str):
                task_data = json.loads(task_data)

            action = task_data.get("action")
            parameters = task_data.get("parameters", {})

            print(f"[DEBUG] Parsed action: {action}, parameters: {parameters}")

            if action == "generate_image":
                image_path = image_gen.generate_image(**parameters)
                message = "Sir, I have generated the image as you told. I will show it to you in a moment."
                print(f"[INFO] {message}")
                TTS.tts.speak(message)
                time.sleep(3)
                show_image(image_path)

            elif action in AUTOMATION_TASKS:
                print(f"[INFO] Executing task: {action} with parameters: {parameters}")
                AUTOMATION_TASKS[action](**parameters)

                with open("last_automation.json", "w") as f:
                    json.dump({"last_action": action, "parameters": parameters}, f)

            elif action == "control_pc":
                start_control_pc()

            elif action == "stop_control_pc":
                stop_control_pc()

            else:
                print(f"[ERROR] No matching automation module found for action: {action}")

        else:
            print("[ERROR] Failed to classify query properly.")

    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON response: {e}")
    except Exception as e:
        print(f"[ERROR] Failed to classify task: {e}")

def show_image(image_path):
    """Display generated image."""
    if os.path.exists(image_path):
        try:
            if os.name == "nt":
                os.startfile(image_path)
            elif os.name == "posix":
                subprocess.run(["xdg-open", image_path], check=True)
            print(f"[INFO] Displaying image: {image_path}")
        except Exception as e:
            print(f"[ERROR] Failed to open image: {e}")
    else:
        print("[ERROR] Image file not found.")

def start_control_pc():
    """Start PC control mode."""
    global control_process
    if control_process is None:
        control_process = subprocess.Popen(["python", "AUTOMATION/controller.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("[INFO] Control PC mode started.")
    else:
        print("[INFO] Control PC mode is already running.")

def stop_control_pc():
    """Stop PC control mode."""
    global control_process
    if control_process is not None:
        control_process.terminate()
        control_process = None
        print("[INFO] Control PC mode stopped.")
    else:
        print("[INFO] Control PC mode is not running.")
