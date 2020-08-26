import requests

def get_weather(city_name, nb_day):
  insee = requests.get(f"https://api.meteo-concept.com/api/location/cities?token=0730ffab58edd00ad6c0eb0174a05d2090a3d91f0f4da4267c7d931db892091b&search={city_name}").json()["cities"][0]["insee"]

  weather_data = requests.get(f"https://api.meteo-concept.com/api/forecast/daily?token=0730ffab58edd00ad6c0eb0174a05d2090a3d91f0f4da4267c7d931db892091b&insee={insee}").json()["forecast"][nb_day]
  
  return [weather_data[i] for i in ("datetime", "wind10m", "gust10m", "dirwind10m", "probarain", "tmin", "tmax", "probafrost", "probafog")]
