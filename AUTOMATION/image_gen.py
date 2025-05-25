import requests
import os
import base64
import time
import threading
from dotenv import load_dotenv
from PIL import Image

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Hugging Face API URL for Stable Diffusion
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Default output path
OUTPUT_PATH = "generated_image.png"

def generate_image(description: str, output_path=OUTPUT_PATH):
    """Generates an image based on a text prompt using the Hugging Face API."""
    
    if not API_KEY:
        print("[ERROR] Hugging Face API key is missing in .env file.")
        return "Error: Missing API key."

    print(f"[INFO] Generating image for prompt: {description}")

    headers = {"Authorization": f"Bearer {API_KEY}"}
    data = {"inputs": description}

    try:
        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            image_data = response.content

            # Save image
            with open(output_path, "wb") as f:
                f.write(image_data)

            print(f"[SUCCESS] Image saved as {output_path}")

            # Automatically display image
            display_image(output_path)

            # Start a background thread to delete the image after 1 minute
            threading.Thread(target=delete_image_later, args=(output_path,), daemon=True).start()
            return f"Image generated successfully: {output_path}"

        else:
            print(f"[ERROR] Failed to generate image: {response.status_code} - {response.text}")
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        print(f"[ERROR] Exception during image generation: {e}")
        return f"Error generating image: {e}"

def display_image(image_path):
    """Opens the generated image."""
    try:
        img = Image.open(image_path)
        img.show()
    except Exception as e:
        print(f"[ERROR] Failed to display image: {e}")

def delete_image_later(image_path):
    """Deletes the generated image after 1 minute."""
    time.sleep(40)  # Wait 40 seconds
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
            print(f"[INFO] Image {image_path} deleted after 1 minute.")
        except Exception as e:
            print(f"[ERROR] Failed to delete image: {e}")

if __name__ == "__main__":
    while True:
        user_query = input("Enter your image description: ").strip().lower()
        generate_image(user_query)
