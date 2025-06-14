from PIL import Image, ImageTk

def get_weather_icon(temperature):
    if temperature <= 0:
        return "cold.png"
    elif 1 <= temperature <= 25:
        return "cloud.png"
    elif temperature > 25:
        return "sun.png"
    return "cloud.png"


def update_gui(location, output_area, weather_icon):
    from weather_fetcher import data_lock, weather_data, stopped_threads

    def update():
        with data_lock:
            if location in weather_data:
                output_area.configure(state="normal")
                output_area.delete(1.0, "end")
                data = weather_data[location]
                for key, value in data.items():
                    if key != "TemperatureValue":
                        output_area.insert("end", f"{key}: {value}\n")
                output_area.configure(state="disabled")

                # Update icon
                icon_path = get_weather_icon(data["TemperatureValue"])
                try:
                    icon_image = Image.open(icon_path).resize((100, 100))
                    icon_photo = ImageTk.PhotoImage(icon_image)
                    weather_icon.configure(image=icon_photo)
                    weather_icon.image = icon_photo
                except Exception as e:
                    print(f"Error loading weather icon: {str(e)}")

        if not stopped_threads:
            weather_icon.after(3000, update)

    update()
