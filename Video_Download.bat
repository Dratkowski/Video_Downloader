@echo off

:: Change directory to the yt-dlp folder
cd C:\Users\Research\yt-dlp

:: Check if the virtual environment exists
IF NOT EXIST ytdlp_venv\Scripts\activate.bat (
    echo Virtual environment not found! Exiting...
    pause
    exit /b
)

:: Activate the virtual environment
call ytdlp_venv\Scripts\activate.bat

:: Run the Python script
python Video_downloader.py

:: Deactivate the virtual environment after the script finishes
deactivate

:: Pause to keep the window open
pause