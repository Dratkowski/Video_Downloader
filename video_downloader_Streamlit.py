import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import subprocess
import os
from urllib.parse import urlparse

# --- Helper function ---
def extract_video_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        video_extensions = r'(https?://[^\s]+(\.mp4|\.m3u8|\.webm|\.avi|\.mov))'
        video_links = re.findall(video_extensions, soup.prettify())
        return [link[0] for link in video_links]
    except Exception as e:
        st.error(f"Error fetching URL: {e}")
        return []

# --- Streamlit UI ---
st.title("🎥 Video Link Extractor and Downloader")

# 1. URL input
url = st.text_input("Enter Website URL to Extract Video Links")

# 2. Filename input
filename = st.text_input("Enter custom file name (saved to Desktop)", value="default_filename")

# 3. Download type selector
download_option = st.selectbox(
    "Select video option (match to file extension)",
    ["Youtube", ".m3u8", "MP4/Social Media Videos"]
)

# Extract links button
if st.button("🔍 Extract Video Links"):
    if not url:
        st.warning("Please enter a URL.")
    else:
        if "facebook.com" in url:
            st.session_state.video_links = [url]
        else:
            found_links = extract_video_links(url)
            st.session_state.video_links = found_links if found_links else [url]
            if not found_links:
                st.info("No links found. Using entered URL as default.")

# Show video link options
if "video_links" in st.session_state and st.session_state.video_links:
    selected_video = st.selectbox("Select a video link to download", st.session_state.video_links)

    # Download button
    if st.button("⬇️ Download Video"):
        try:
            # Determine download path
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            output_path = os.path.join(desktop_path, filename)

            # Fix extension if needed
            if selected_video.lower().endswith(".mp4") and not output_path.endswith(".mp4"):
                output_path += ".mp4"
            elif download_option in [".m3u8", "MP4/Social Media Videos"] and not output_path.endswith(".mp4"):
                output_path += ".mp4"

            # Run yt-dlp
            st.info(f"Downloading to: {output_path}")
            subprocess.run(["yt-dlp", "-o", output_path, selected_video], check=True)

            # Convert .webm to .mp4 if Youtube
            if download_option == "Youtube":
                webm_file = f"{output_path}.webm"
                mp4_file = f"{output_path}.mp4"
                subprocess.run(["ffmpeg", "-i", webm_file, mp4_file], check=True)
                os.remove(webm_file)
                st.success(f"Downloaded and converted: {mp4_file}")
            else:
                st.success(f"Download complete: {output_path}")

        except Exception as e:
            st.error(f"Download failed: {e}")
