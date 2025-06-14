import customtkinter as ctk
from gui import setup_main_window

def main():
    # Set appearance mode and theme
    ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

    # Create the main window
    main_window = ctk.CTk()
    main_window.title("Weather Data Aggregator")
    main_window.geometry("600x300")
    main_window.resizable(False, False)

    # Setup the GUI
    setup_main_window(main_window)

    main_window.mainloop()


if __name__ == "__main__":
    main()
