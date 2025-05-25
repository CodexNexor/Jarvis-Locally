import webbrowser
import time
import requests
from bs4 import BeautifulSoup

GMAIL_URL = "https://mail.google.com/mail/u/0/#inbox"

def get_unread_email_count():
    """Scrapes Gmail to check the number of unread emails."""
    print("[INFO] Opening Gmail...")

    # Open Gmail in the default browser
    webbrowser.open(GMAIL_URL)

    # Wait for user to log in and Gmail to load
    time.sleep(10)

    # Fetch Gmail page source (requires user to be logged in)
    response = requests.get(GMAIL_URL)

    if response.status_code != 200:
        print("[ERROR] Failed to fetch Gmail inbox. Make sure you're logged in.")
        return None

    # Parse the page source to find the unread email count
    soup = BeautifulSoup(response.text, "html.parser")
    unread_count_element = soup.find("div", class_="bsU")

    if unread_count_element:
        unread_count = unread_count_element.text.strip()
        print(f"[INFO] Sir, you have {unread_count} unread emails. Please check them.")
    else:
        print("[INFO] No unread emails found.")

# Example usage
if __name__ == "__main__":
    get_unread_email_count()

    import webbrowser

def execute_task():
    """Check new emails by opening Gmail."""
    gmail_url = "https://mail.google.com/mail/u/0/#inbox"
    print("[INFO] Checking Gmail inbox.")
    
    # Open Gmail in the default browser
    webbrowser.open(gmail_url)

# Example usage (for manual testing)
if __name__ == "__main__":
    execute_task()

