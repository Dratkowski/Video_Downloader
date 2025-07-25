import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import subprocess
import os
import tempfile

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
filename = st.text_input("Enter custom file name (for browser download)", value="default_filename")

# 3. Download type selector
download_option = st.selectbox(
    "Select video option (used for labeling only)",
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
                st.info("No direct links found. Using entered URL as fallback.")

# Show video link options
if "video_links" in st.session_state and st.session_state.video_links:
    selected_video = st.selectbox("Select a video link to download", st.session_state.video_links)

    # Download button
    if st.button("⬇️ Download Video"):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                temp_path = tmp_file.name

            # Download with yt-dlp
            st.info("Downloading... this may take a moment.")
            subprocess.run(["yt-dlp", "-o", temp_path, selected_video], check=True)

            # Read file
            with open(temp_path, "rb") as f:
                video_bytes = f.read()

            # Streamlit browser download
            st.download_button(
                label="📥 Click here to download the video",
                data=video_bytes,
                file_name=f"{filename}.mp4",
                mime="video/mp4"
            )

            os.remove(temp_path)

        except Exception as e:
            st.error(f"Download failed: {e}")
