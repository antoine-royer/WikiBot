import requests
import os

def get_weather(city_name, day):
  api_key = os.environ["weather_token"]
  weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}").json()

  lon, lat = weather_data["coord"]["lon"], weather_data["coord"]["lat"]
  weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly&appid={api_key}").json()["daily"][day]

  return (
    weather_data["weather"][0]["description"],
    int(weather_data["temp"]["day"] - 273.15),
    int(weather_data["feels_like"]["day"] - 273.15),
    int(weather_data["dew_point"] - 273.15),
    weather_data["pressure"],
    weather_data["humidity"],
    int(weather_data["wind_speed"] * 3.6),
    weather_data["wind_deg"],
    weather_data["clouds"],
    weather_data["pop"] * 100,
    weather_data["timezone"],
    f'https://openweathermap.org/img/w/{weather_data["weather"][0]["icon"]}.png')
