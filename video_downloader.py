import tkinter as tk
from tkinter import ttk
import subprocess
import webbrowser
from urllib.parse import urlparse
import os

# Function to execute yt-dlp with the given URL and custom file name
def download_video():
    url = url_entry.get()  # Get the URL from the input field
    custom_filename = filename_entry.get()  # Get the custom file name from the entry box
    download_option = download_option_combobox.get()  # Get the selected option ("Youtube", ".m3u8", or "MP4/Facebook")
    
    # Get the user's Desktop path dynamically
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    if not custom_filename:
        # If no custom filename, use the default based on the URL (just use the domain for simplicity)
        parsed_url = urlparse(url)
        custom_filename = parsed_url.netloc

    # Update custom_filename to save it on the Desktop
    custom_filename = os.path.join(desktop_path, custom_filename)

    # If the "MP4" option is selected, check if the URL is already .mp4 and keep the filename
    if download_option == "MP4" and url.lower().endswith(".mp4"):
        custom_filename = custom_filename if custom_filename.endswith(".mp4") else custom_filename + ".mp4"
        download_option = "MP4"  # Keep it as MP4 for download option

    # If .m3u8 is selected, automatically add ".mp4" to the file name
    elif download_option == ".m3u8" and not custom_filename.endswith(".mp4"):
        custom_filename += ".mp4"
    
    # If MP4/Facebook is selected, add ".mp4" to the file name if not already present
    elif download_option == "MP4/Facebook" and not custom_filename.endswith(".mp4"):
        custom_filename += ".mp4"
    
    if url:
        try:
            # Run yt-dlp command with the URL entered and the custom filename
            subprocess.run(["yt-dlp", "-o", custom_filename, url])
            
            # If Youtube is selected, convert the downloaded .webm to .mp4
            if download_option == "Youtube":
                webm_file = f"{custom_filename}.webm"
                mp4_file = f"{custom_filename}.mp4"
                # Run ffmpeg to convert .webm to .mp4
                subprocess.run(["ffmpeg", "-i", webm_file, mp4_file])
                
                # Optionally, remove the original .webm file after conversion
                os.remove(webm_file)  # Removes the .webm file after conversion
                
                # Update result label with the new .mp4 file path
                result_text = f"Download and conversion finished: {mp4_file}"
            else:
                result_text = f"Download finished: {custom_filename}"
            
            # Display the result with the link to the file
            result_label.config(text=result_text, fg="blue", cursor="hand2")
            result_label.bind("<Button-1>", lambda e: open_link(custom_filename))
            
            # Show the "Run Again" button after a successful download
            run_again_button.pack(pady=10)

        except Exception as e:
            result_label.config(text=f"Error: {e}")
    else:
        result_label.config(text="Please enter a Youtube URL or .m3u8 file:")

# Function to open the path or URL when the label is clicked 
def open_link(link): 
    try: 
        # Open the file path or URL 
        webbrowser.open(f'file:///{link}' if link.startswith('C:\\') else link) 
    except Exception as e: 
        print(f"Error opening link: {e}") 

# Function to reset the form and allow a new URL to be entered
def run_again():
    # Clear the input fields
    url_entry.delete(0, tk.END)
    filename_entry.delete(0, tk.END)
    download_option_combobox.set("Youtube")  # Reset to default "Youtube"
    
    # Hide the "Run Again" button again until the next download
    run_again_button.pack_forget()
    
    # Clear the result label
    result_label.config(text="")

# Set up the main application window 
root = tk.Tk() 
root.title("yt-dlp GUI") 

# URL label and input field 
url_label = tk.Label(root, text="Please enter a Youtube URL or file:") 
url_label.pack(pady=10) 

# URL entry box 
url_entry = tk.Entry(root, width=100) 
url_entry.pack(padx=20, pady=10) 

# File name label and entry box 
filename_label = tk.Label(root, text="Enter custom file name") 
filename_label.pack(pady=10) 

filename_entry = tk.Entry(root, width=100) 
filename_entry.pack(padx=20, pady=10) 

# Set default file name based on URL (this can be changed later by the user) 
filename_entry.insert(0, "default_filename") 

# Dropdown box to select "Youtube", ".m3u8", or "MP4/Facebook"
download_option_label = tk.Label(root, text="Select download option:") 
download_option_label.pack(pady=10) 

download_option_combobox = ttk.Combobox(root, values=["Youtube", ".m3u8", "MP4/Facebook"], state="readonly") 
download_option_combobox.pack(padx=20, pady=10)
download_option_combobox.set("Youtube")  # Set default option

# Button to start the download
download_button = tk.Button(root, text="Download", command=download_video)
download_button.pack(pady=10)

# Label to display result or error message
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# Button to run the program again after the download is complete
run_again_button = tk.Button(root, text="Run Again", command=run_again)
run_again_button.pack_forget()  # Hide it initially

# Run the Tkinter event loop
root.mainloop()
