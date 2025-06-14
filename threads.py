import threading
from weather_fetcher import fetch_weather  # Import fetch_weather
from gui import create_location_window
import customtkinter as ctk

location_windows = {}
stopped_threads = False


stopped_threads = False

def start_fetching(location_entry, main_window):
    global stopped_threads, location_windows
    stopped_threads = False

    locations = location_entry.get().split(",")
    

    for idx, location in enumerate(locations):
        location = location.strip()
        if location:
            if location in location_windows and location_windows[location]:
                location_windows[location].destroy()

            location_window = create_location_window(main_window, location, location_windows)

            # Start weather data fetching in a separate thread
            fetch_thread = threading.Thread(target=fetch_weather, args=(location,), daemon=True)
            fetch_thread.start()

            location_windows[location] = location_window

def stop_fetching():
    global stopped_threads
    stopped_threads = True