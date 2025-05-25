import webbrowser
import requests
from urllib.parse import quote

def get_first_video_url(song_name):
    """Fetches the first video link for a YouTube search query."""
    search_url = f"https://www.youtube.com/results?search_query={quote(song_name)}"
    
    # Get YouTube search results page source
    response = requests.get(search_url)
    if response.status_code != 200:
        print("[ERROR] Failed to fetch YouTube search results.")
        return None

    # Extract the first video URL from the search results
    video_id_start = response.text.find("/watch?v=")
    if video_id_start == -1:
        print("[ERROR] No video found.")
        return None

    video_id = response.text[video_id_start:video_id_start+20].split('"')[0]  # Extract video ID
    return f"https://www.youtube.com{video_id}"

def search_and_play_song(song_name):
    """Searches for a song on YouTube and plays the first result automatically."""
    print(f"[INFO] Searching for '{song_name}' on YouTube...")

    # Get the first video URL
    video_url = get_first_video_url(song_name)
    if video_url:
        print(f"[INFO] Playing: {video_url}")
        webbrowser.open(video_url)
    else:
        print("[ERROR] Could not find a valid video.")

# Example usage
if __name__ == "__main__":
    song_name = input("Enter song name: ")
    search_and_play_song(song_name)


import webbrowser

def execute_task(song):
    """Search for a song on YouTube and play the first result."""
    youtube_search_url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
    print(f"[INFO] Playing '{song}' on YouTube.")
    
    # Open the YouTube search in the default browser
    webbrowser.open(youtube_search_url)

# Example usage (for manual testing)
if __name__ == "__main__":
    execute_task("Lose Yourself Eminem")
