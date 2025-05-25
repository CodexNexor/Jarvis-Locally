import sys
import os
import groq
import random
from dotenv import load_dotenv

sys.path.append("C:/Users/DHEERAJ/Desktop/jarvis/brain")

from brain import chatbot
import automation
import realtime
from TTS import tts

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)

# === CLASSIFICATION RULES ===
DECISION_ROLE = (
    "You are a highly accurate classification system.\n"
    "Classify user queries into ONLY ONE of the following categories:\n"
    "- 'chat' → if the user is just talking or asking something general.\n"
    "- 'automation' → if the user wants you to perform an action (like play, open, turn on/off, use camera, control hardware, etc).\n"
    "- 'realtime' → if the user asks for live or current information (like weather, elections, live score, today news, IPL 2024, etc).\n\n"
    "DO NOT GUESS. DO NOT EXPLAIN. JUST RETURN ONE WORD ONLY.\n\n"
    "Examples:\n"
    "- 'Who is Elon Musk?' → chat\n"
    "- 'Tell me a joke' → chat\n"
    "- 'What's the time in New York?' → chat\n"
    "- 'Hey Jarvis, how are you?' → chat\n"
    "- 'Open YouTube and play Alan Walker' → automation\n"
    "- 'Turn off the fan' → automation\n"
    "- 'Show me using the camera' → automation\n"
    "- 'Download this video' → automation\n"
    "- 'Repeat the last action' → automation\n"
    "- 'Search the web for IPL 2024 auction results' → realtime\n"
    "- 'What's the latest news about ISRO?' → realtime\n"
    "- 'How much money is spent in 2024 elections?' → realtime\n"
    "- 'When is the next iPhone launching?' → realtime\n"
)

last_automation_task = None

def classify_and_process_query(query: str):
    global last_automation_task
    try:
        query_lower = query.lower().strip()
        print(f"[QUERY] {query_lower}")

        # === Handle Repeat Commands ===
        if query_lower in {"next", "again", "repeat", "do it again"} and last_automation_task:
            print("[INFO] Repeating last automation task...")
            return handle_automation_task(last_automation_task)

        # === Classification ===
        print("[AI] Classifying query...")
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": DECISION_ROLE},
                {"role": "user", "content": query}
            ]
        )

        result = response.choices[0].message.content.strip().lower()
        print(f"[AI Classification Result] {result}")

        return route_query(result, query)

    except Exception as e:
        print(f"[ERROR] Exception during classification: {e}")
        tts.speak("There was an error processing your request.")
        return None

def route_query(classification: str, query: str):
    global last_automation_task

    if classification == "chat":
        return chatbot.jarvis_response(query)

    elif classification == "automation":
        return handle_automation_task(query)

    elif classification == "realtime":
        print("[ACTION] Routing to realtime module...")
        result = realtime.generate(user_prompt=query, prints=True)
        tts.speak(result)
        return result

    else:
        print(f"[WARNING] Unexpected classification result: {classification}")
        tts.speak("I'm not sure how to handle that request.")
        return None

def handle_automation_task(query: str):
    global last_automation_task
    confirmations = [
        "Of course, Sir.", "Absolutely, Sir.", "Certainly, Sir.", "Right away, Sir.",
        "You got it, Sir.", "I'm on it, Sir.", "Consider it done, Sir.", "At your service, Sir.",
        "Absolutely, I'm on it, Sir.", "Sure thing, Sir.", "Leave it to me, Sir.",
        "Right away, Sir, I'm taking care of it."
    ]
    tts.speak(random.choice(confirmations))
    print("[ACTION] Routing to automation system...")
    last_automation_task = automation.classify_and_route_task(query)
    return None
