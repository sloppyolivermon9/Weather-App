from customtkinter import *
from CTkMessagebox import *
import requests
import json

from dataclasses import dataclass
def getLocation():
    class Location:
        lat : str() = ""
        lon : str() = ""
    location = Location()

    city = CityEntry.get()
    limit = 1

    rawAPIResult = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit={limit}&appid={key}")
    APIResult = json.loads(rawAPIResult.content)
    
    location.lat,location.lon = APIResult[0]["lat"],APIResult[0]["lon"]
    return location

def getWeather():
    class Weather:
        weatherState : str() = ""
        temperature : float() = 0.0
        temperatureFeelsLike : float() = 0.0

    location = getLocation()

    rawAPIResult = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={location.lat}&lon={location.lon}&appid={key}&units=metric")
    APIResult = json.loads(rawAPIResult.content)
    print(APIResult)

    weather = Weather()
    weather.weatherState = APIResult["weather"][0]["description"]
    weather.temperature = APIResult["main"]["temp"]
    weather.temperatureFeelsLike = APIResult["main"]["feels_like"]
    return weather

def main():
    global key
    key = "Your API key here!"

    try:
        weather = getWeather()

        WeatherStateDisplay.configure(text="Weather: " + weather.weatherState)
        TemperatureDisplay.configure(text="Temperature: " + str(weather.temperature) + " °C")
        FeelsLikeDisplay.configure(text="Feels Like: " + str(weather.temperatureFeelsLike) + " °C")
    except:
        errorMessage = CTkMessagebox(title="Error", message="Something went wrong: you didn't enter a correct name or you left it blank", icon="cancel")


set_appearance_mode("dark")  # Modes: system (default), light, dark
set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

MainWindow = CTk()
MainWindow.geometry("500x500")

WindowTitle = CTkLabel(MainWindow, text="Sloppy Weather", font=("Ariel", 26))
WindowTitle.pack()

CityPrompt = CTkLabel(MainWindow, text="Enter city name:", font=("Ariel", 20))
CityPrompt.pack()

CityEntry = CTkEntry(MainWindow)
CityEntry.pack()

Space = CTkLabel(MainWindow, text="")
Space.pack()

WeatherButton = CTkButton(MainWindow, text="Get Weather", command=main)
WeatherButton.pack()

Space1 = CTkLabel(MainWindow, text="")
Space1.pack()

WeatherStateDisplay = CTkLabel(MainWindow, text="Weather: ")
WeatherStateDisplay.pack()

TemperatureDisplay = CTkLabel(MainWindow, text="Temperature: ")
TemperatureDisplay.pack()

FeelsLikeDisplay = CTkLabel(MainWindow, text="Feels Like: ")
FeelsLikeDisplay.pack()

MainWindow.mainloop()
