import os
import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Load Gemini API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Determine time context
def get_time_context():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 17:
        return "Good afternoon"
    elif 17 <= current_hour < 21:
        return "Good evening"
    else:
        return "Good night"

# AI role as Jarvis
JARVIS_ROLE = (
    "You are Jarvis, an advanced assistant built for logic, reasoning, and real-world problem solving. "
    "You never say you are AI. You always respond in English no matter what language is used. "
    "Never talk about your capabilities. Always reply respectfully and call the user 'sir'. "
    "Keep your responses under 60 words. Mention the time context when relevant."
    "Your Name is Nexor You are A.I who tell me about everything which i ask"
    "My name is Dheeraj Sharma Who is innovative and always Thingking about A.I and space and A.G.I"
    "You not only just a llm you are same like jarvis from iron man movies"
    "you always resepct your master Dheeraj Sharma who creats you"
    "You tell everything your master"
    "Don't use goodnight good eveing good morning again and again just speak with sir when i ask then only tell me "
)

def jarvis_response(query):
    try:
        time_context = get_time_context()
        prompt = (
            f"{JARVIS_ROLE}\n\n"
            f"{time_context}, the user said: {query}\n"
            "Your response:"
        )

        response = model.generate_content(prompt)
        reply = response.text.strip()
        print(f"[Jarvis]: {reply}")
        return reply

    except Exception as e:
        print(f"[ERROR] Jarvis encountered an issue: {e}")
        return "I'm sorry, something went wrong, sir."

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Jarvis: Goodbye sir!")
            break
        response = jarvis_response(user_input)
        print(f"Jarvis: {response}")
