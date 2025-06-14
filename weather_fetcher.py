import random
import threading
import time

# Shared data and lock
weather_data = {}
data_lock = threading.Lock()

# Flag to stop threads
stopped_threads = False

def fetch_weather(location):
    global weather_data, stopped_threads
    while not stopped_threads:
        try:
            with data_lock:
                # Simulate weather data
                temperature = random.randint(-10, 45)
                humidity = random.randint(0, 100)
                wind_speed = random.randint(0, 100)
                wind_direction = random.choice(["N", "S", "E", "W", "NE", "NW", "SE", "SW"])
                pressure = random.randint(950, 1050)

                # Update weather data
                weather_data[location] = {
                    "Temperature": f"{temperature}°C",
                    "Humidity": f"{humidity}%",
                    "Wind Speed": f"{wind_speed}km/h",
                    "Wind Direction": wind_direction,
                    "Pressure": f"{pressure} hPa",
                    "TemperatureValue": temperature
                }
        except Exception as e:
            print(f"Error fetching weather data for {location}: {str(e)}")

        time.sleep(3)


def stop_fetching():
    global stopped_threads
    stopped_threads = True
