# Video_Downloader
yt-dlp (https://github.com/yt-dlp/yt-dlp)

yt-dlp is a simple program that downloads a variety to videos from websites (including Youtube.com). Typiclaly, in order to download Youtube videos, a paid subscription to Youtube Premium. It is a very simple program to install. Just ensure python is installed. See Transcription_Tool repo for more on python.

STEP 1: Creat a Virtual Environment
When creating a new program, it is a good idea to make a virtual enviornment to run the program. This environment is where all of the libraries and dependencies will be installed. It Keep things seperate from other programs so dependencies are not impacted by other tools. 
      Dependencies/Libraries: Simply put these are tools that other programers and coders have developed to run sertain things with         the code. These help you do a wide variety of things so you do not have to do all the coding yourself. 
      
  STEP 1A: Set up a virtual environment (venv)
  
  1) Create a new folder on your C: drive labled "yt-dlp" (or something like that)
  2) Right click within that new folder, and "OPEN IN TERMINAL" (You can also open PowerShell and type: cd "C:file\path\to\your\new\folder"). "cd" is the command to open a folder directory
       path.
       
         cd "C:file\path\to\your\new\folder"
     
  4) Now create the virtual environment by typing in terminal:

         python -m venv NAME_YOUR_VENV
     
      Example:
     
         python -m venv yt-dlp_venv
          
  5) Once the venv is created in your directory, you need to activate the venv. This opens the venv and will store all of your dependencies within the venv. You will know you are in the venv when you see the name of your venv in green before your directory file path.
       Acttivate your venv:

         YOUR_VENV\Scripts\activate
     Example:

         yt-dlp_venv\Scripts\activate
STEP 2) 
Now that your venv is active, you can install Whisper within this venv. NOTE: if you close the terminal you will need to reactivate the venv. Make sure that you have downloaded the file "requirements.txt" and place it in your directory
      Installing dependencies:

    pip install -r requirements.txt

  "pip" is the code you will use to install most python libraries and dependencies.
  
  1) Verify that all the dependencies installed correctly. This list should have all the same things as the requierments.txt

         pip list

Create a file to store the .py file and download the three .py files. 

    Video_scrub.py = will scrub a website for .mp4, .m3u8, .webm, .avi, .mov
    
    video_dowloader.py = will run a basic GUI to help you download Youtube videos, .m3u8, and .mp4

    Full_scrubber_and_download = will run both the above together in one program

  These can be run in Terminal/PowerShell

    python Video_scrub.py

    python video_dowloader.py

    python Full_scrubber_and_download

OR 

They can be run by creating a .bat file that can be placed on your desktop and run similar to a desktop program. 
Download the individual .bat files and remember to edit the file to indicate where your yt-dlp_venv is stored.

You can also open a Notepad copy paste:
    
    @echo off

    :: Change directory to the yt-dlp folder
    cd LOCATION\OF\YOUR\DIRECTORY\yt-dlp

    :: Check if the virtual environment exists
    IF NOT EXIST ytdlp_venv\Scripts\activate.bat (
        echo Virtual environment not found! Exiting...
        pause
        exit /b
    )

    :: Activate the virtual environment
    call ytdlp_venv\Scripts\activate.bat

    :: Run the Python script CHANGE THIS TO INDICATE WHICH .PY FILE YOU WANT TO RUN
    python Full_scruber_and_download.py

    :: Deactivate the virtual environment after the script finishes
    deactivate

    :: Pause to keep the window open
    pause

Save as a .bat file on your desktop
