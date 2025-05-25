import time
from STT import stt
from brain import decision
from TTS import tts

def start_stt():
    """Listens for speech input and processes it only if it starts with 'Jarvis'."""
    print("[INFO] Starting STT...")

    while True:
        query = stt.listen()  # Always listening

        if query:
            print(f"[DEBUG] User Query: {query}")  # Debugging

            # Check if the query starts with "Jarvis"
            if query.lower().startswith("jarvis"):
                process_query(query)
            else:
                print("[INFO] Ignoring query as it does not start with 'Jarvis'.")

        time.sleep(0.5)  # Small delay to prevent excessive looping

def process_query(query):
    """Processes the user's speech by sending it to decision.py."""
    print(f"[Jarvis]: Processing query...")

    response = decision.classify_and_process_query(query)  # Decision handles chat & automation

    # Speak the response ONLY if it's a chat response
    if response:
        print(f"[Jarvis]: {response}")

        # Stop listening while speaking
        stt.pause_listening(True)  
        tts.speak(response)  # Speak only chat responses
        time.sleep(1)  # Wait a bit to avoid instant reactivation
        stt.pause_listening(False)  # Resume listening

if __name__ == "__main__":
    print("[INFO] Jarvis is now running...")
    start_stt()  # Start listening and processing queries
