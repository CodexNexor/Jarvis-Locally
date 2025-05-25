import cv2
import os
import time
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
from TTS.tts import speak  # Uses Jarvis' TTS module

# Load Gemini API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')

def capture_image(filename="vision_capture.jpg"):
    """Capture image from webcam"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not accessible.")
        speak("Sir, I cannot access the camera.")
        return None

    print("Capturing image, sir...")
    speak("Capturing image now, sir.")
    ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()

    if ret:
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}.")
        return filename
    else:
        print("Failed to capture image.")
        speak("I failed to capture the image, sir.")
        return None

def ask_gemini_about_image(image_path: str, prompt: str = "Describe everything you see in this image."):
    """Send image and prompt to Gemini, then delete image"""
    try:
        # Use context manager to auto-close image
        with Image.open(image_path) as image:
            image.load()  # Force load into memory

            # Send to Gemini
            response = model.generate_content(
                [prompt, image],
                stream=False
            )

        # Now image is closed, we can delete safely
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted image {image_path} after analysis.")

        answer = response.text.strip()
        return f"Sir, {answer}"

    except Exception as e:
        return f"Sir, I encountered an error while analyzing the image: {e}"

def execute_task():
    """Main visual analysis function for Jarvis"""
    image_path = capture_image()
    if image_path:
        speak("Processing image with Gemini visual model.")
        result = ask_gemini_about_image(image_path)
        print(result)
        speak(result)
    else:
        speak("Sir, I could not complete the visual task.")
