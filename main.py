# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import clr
import os
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from dotenv import load_dotenv
import sys

# clr.AddReference(r"C:\Users\olir\Documents\RMC2\FIrefoxScanner\ProgramAudio\ProgramAudio\bin\Debug\net9.0\ProgramAudio.dll")
# Get the base directory of the executable (or script during development)
base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Path to the DLLs (adjust to match the relative destination specified in --add-data)
dll_folder = os.path.join(base_dir, r"FirefoxScanner\ProgramAudio\ProgramAudio\bin\Debug\net9.0")  # Matches the relative destination specified in --add-data
dll_path = os.path.join(dll_folder, "ProgramAudio.dll")

# Load the DLL
clr.AddReference(dll_path)

from ProgramAudio import AudioChecker



load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-read-playback-state user-modify-playback-state"))
def pause_spotify():
    sp.pause_playback()

def resume_spotify():
    sp.start_playback()

def is_spotify_playing():
    playback = sp.current_playback()
    return playback and playback['is_playing']



def is_firefox_playing():
    return AudioChecker.IsFirefoxPlaying()

def background_task():
    was_spotify_playing = False

    while running:
        firefox_playing = is_firefox_playing()
        spotify_playing = is_spotify_playing()

        if firefox_playing and spotify_playing:
            print("YouTube is playing; pausing Spotify.")
            pause_spotify()
            was_spotify_playing = True

        elif not firefox_playing and not spotify_playing and was_spotify_playing:
            print("YouTube paused; resuming Spotify.")
            resume_spotify()
            was_spotify_playing = False

        time.sleep(1)



def create_tray_icon():
    global icon

    # Create images for the tray icon
    global image_running, image_stopped
    image_running = Image.new('RGB', (64, 64), color=(0, 255, 0))  # Green when running
    draw = ImageDraw.Draw(image_running)
    draw.text((10, 20), "Running", fill="white")

    image_stopped = Image.new('RGB', (64, 64), color=(255, 0, 0))  # Red when stopped
    draw = ImageDraw.Draw(image_stopped)
    draw.text((10, 20), "Stopped", fill="white")

    # Define the context menu for the tray icon
    menu = (item('Start', start_program), item('Stop', stop_program))

    # Create the icon and run it
    icon = pystray.Icon("Music Canceller", image_stopped, menu=menu)
    icon.run()


# Global variable to track the program state
running = False

# Function to stop the background task (used by the exit menu item)
def stop_program(icon, item):
    global running
    running = False
    icon.icon = image_stopped
    icon.update_menu()

# Function to start the background task (used by the start menu item)
def start_program(icon, item):
    global running
    running = True
    task_thread = threading.Thread(target=background_task)
    task_thread.daemon = True
    task_thread.start()
    icon.icon = image_running
    icon.update_menu()

running = False
def main():

    # Create the tray icon
    create_tray_icon()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
