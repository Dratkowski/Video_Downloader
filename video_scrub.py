import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import re

# Function to extract video file paths
def extract_video_links(url):
    try:
        # Send GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Regular expression to match video file types
        video_extensions = r'(https?://[^\s]+(\.mp4|\.m3u8|\.webm|\.avi|\.mov))'
        
        # Find all video links
        video_links = re.findall(video_extensions, soup.prettify())
        
        # Return only the URLs (without the tuple)
        return [link[0] for link in video_links]
    except requests.exceptions.RequestException as e:
        # Handle request errors
        messagebox.showerror("Error", f"Failed to fetch the URL: {e}")
        return []

# Function to handle the button click
def on_search_button_click():
    # Get the URL from the user input
    url = url_entry.get()

    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL")
        return

    # Extract video links
    video_links = extract_video_links(url)

    # Clear the previous results
    result_text.delete(1.0, tk.END)

    # Display the results
    if video_links:
        result_text.insert(tk.END, "\n".join(video_links))
    else:
        result_text.insert(tk.END, "No video links found.")

# Set up the main window
root = tk.Tk()
root.title("Video Link Extractor")

# URL Input Label and Entry
url_label = tk.Label(root, text="Enter Website URL:")
url_label.pack(pady=5)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Search Button
search_button = tk.Button(root, text="Search for Videos", command=on_search_button_click)
search_button.pack(pady=10)

# Textbox to display results
result_text = tk.Text(root, height=15, width=60)
result_text.pack(pady=5)

# Run the application
root.mainloop()
