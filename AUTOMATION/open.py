import json
import os
import subprocess
import webbrowser

def load_websites():
    """Loads website data from websites.json."""
    json_file = "C:\\Users\\DHEERAJ\\Desktop\\jarvis\\Assists\\websites.json"
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def open_application_or_website(name):
    """Opens a website if found in the dictionary, otherwise searches for an app."""
    websites = load_websites()
    
    # Check if it's a website
    for site_name, url in websites.items():
        if name.lower() in site_name.lower():
            print(f"Opening website: {url}")
            webbrowser.open(url)
            return
    
    # Otherwise, try opening an application
    print(f"Opening application: {name}")
    try:
        subprocess.run(["start", "", name], shell=True, check=True)
    except Exception as e:
        print(f"[ERROR] Failed to open application: {e}")

# Example usage (you can remove this in actual implementation)
if __name__ == "__main__":
    query = input("Enter app or website name: ")
    open_application_or_website(query)
def execute_task(name):
    """Handles execution when called by automation.py."""
    open_application_or_website(name)