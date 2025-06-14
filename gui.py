import customtkinter as ctk
from weather_fetcher import fetch_weather, stop_fetching
from utils import update_gui
import tkinter.messagebox as messagebox 
# Store the reference to the last opened window for each location
location_windows = {}

def validate_location(location):
    """Validates the location name."""
    location = location.strip()
    if len(location) < 4:
        return "Location must have at least 4 characters."
    if all(char == location[0] for char in location):
        return "Location cannot have all identical characters."
    if ", " in location or " ," in location:
        return "Location cannot contain improper spacing with commas."
    return None 

def start_fetching(location_entry, main_window):
    global location_windows
    locations = location_entry.get().split(",")
    for location in locations:
        location = location.strip()
        error_message = validate_location(location)
        if error_message:
            messagebox.showerror("Invalid Location", f"Error in location '{location}': {error_message}")
            return  # Stop execution if any location is invalid
    # Calculate positions for centering windows beside each other
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    window_width, window_height = 400, 300  # Window dimensions
    x_offset = (screen_width - window_width * len(locations)) // 2
    y_offset = (screen_height - window_height) // 2

    for idx, location in enumerate(locations):
        location = location.strip()
        if location:
            # Close the last window for this location if it exists
            if location in location_windows and location_windows[location]:
                location_windows[location].destroy()

            # Create a new Toplevel window for this location
            location_window = ctk.CTkToplevel(main_window)
            location_window.title(f"Weather Data for {location}")
            window_x = x_offset + (idx * window_width)
            location_window.geometry(f"{window_width}x{window_height}+{window_x}+{y_offset}")

            # Add content to the window
            add_location_window_content(location_window, location)

            # Store the reference to the location window
            location_windows[location] = location_window


def add_location_window_content(window, location):
    from weather_fetcher import data_lock, weather_data
    import threading

    # Frame to hold weather data
    location_frame = ctk.CTkFrame(window, corner_radius=10)
    location_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Label for the location name
    ctk.CTkLabel(location_frame, text=f"Weather Data for {location}",
                 font=("Arial", 16, "bold")).pack(pady=5)

    # Label for weather icon
    weather_icon = ctk.CTkLabel(location_frame)
    weather_icon.pack(pady=5)

    # Text widget for weather data
    output_area = ctk.CTkTextbox(location_frame, wrap="word", height=200, width=300, font=("Arial", 12))
    output_area.pack(padx=10, pady=10, fill="both", expand=True)
    output_area.configure(state="disabled")

    # Start threads for fetching and updating the location window's GUI
    fetch_thread = threading.Thread(target=fetch_weather, args=(location,), daemon=True)
    fetch_thread.start()

    update_gui(location, output_area, weather_icon)  # Start the GUI update loop for this location


def setup_main_window(main_window):
    input_frame = ctk.CTkFrame(main_window, corner_radius=10)
    input_frame.pack(pady=20, padx=20, fill="both", expand=True)

    ctk.CTkLabel(input_frame, text="Enter locations separated by commas:", font=("Arial", 14)).pack(pady=10)

    location_entry = ctk.CTkEntry(input_frame, width=400, font=("Arial", 12))
    location_entry.pack(pady=5)

    button_frame = ctk.CTkFrame(input_frame, corner_radius=10)
    button_frame.pack(pady=10)

    ctk.CTkButton(button_frame, text="Start Fetching", font=("Arial", 12),
                  command=lambda: start_fetching(location_entry, main_window)).pack(side="left", padx=10)
    ctk.CTkButton(button_frame, text="Stop Fetching", font=("Arial", 12), command=stop_fetching).pack(side="right", padx=10)
