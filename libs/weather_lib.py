import requests
import os
import time

def get_weather(city_name, day):
  api_key = os.environ["weather_token"]

  weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}").json()

  lon, lat = weather_data["coord"]["lon"], weather_data["coord"]["lat"]
  weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly&appid={api_key}").json()
  datetime = time.ctime(weather_data["daily"][day]["dt"])

  return (
    weather_data["daily"][day]["weather"][0]["description"],
    int(weather_data["daily"][day]["temp"]["day"] - 273.15),
    int(weather_data["daily"][day]["feels_like"]["day"] - 273.15),
    int(weather_data["daily"][day]["dew_point"] - 273.15),
    weather_data["daily"][day]["pressure"],
    weather_data["daily"][day]["humidity"],
    int(weather_data["daily"][day]["wind_speed"] * 3.6),
    weather_data["daily"][day]["wind_deg"],
    weather_data["daily"][day]["clouds"],
    int(weather_data["daily"][day]["pop"] * 100),
    weather_data["timezone"],
    f'https://openweathermap.org/img/w/{weather_data["daily"][day]["weather"][0]["icon"]}.png',
    f"{datetime[0:3]} {datetime[8:10].replace(' ', '')} {datetime[4:7]} {datetime[-4:]}")
