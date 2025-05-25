import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Import decision and chatbot modules
from brain import decision
import TTS.tts  

# Chrome options setup
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")  

# Path to ChromeDriver
chrome_driver_path = "C:\\Users\\DHEERAJ\\Desktop\\jarvis\\STT\\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

# Initialize WebDriver once (fixes reconnection error)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://allorizenproject1.netlify.app/")

# Control flag to pause listening
pause = False  

def pause_listening(status):
    """Pause or resume STT listening."""
    global pause
    pause = status

def listen():
    """Continuously listens for speech input but pauses when speaking."""
    global pause
    print("[INFO] Listening...")

    try:
        # Wait for the start button once
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()

        previous_text = ""

        while True:
            if pause:  
                time.sleep(0.5)  # When paused, do nothing
                continue  

            # Get recognized speech
            output_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'output')))
            recognized_text = output_element.text.strip().lower()

            if recognized_text and recognized_text != previous_text:
                print("[User]:", recognized_text)
                previous_text = recognized_text
                return recognized_text  # Send text for processing

            time.sleep(0.5)  # Small delay to avoid overloading

    except Exception as e:
        print("[ERROR] STT Error:", e)

    return ""  # If error occurs, return empty string
