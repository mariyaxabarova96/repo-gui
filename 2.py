import requests
import json

city = input('Name of city ')
api = '899854cd245220707c74df200e599cd2'
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                 params={'q': city, 'units': 'metric', 'APPID': api})
data = res.json()
print("temp:", data['main']['temp'])
print("temp_min:", data['main']['temp_min'])
print("temp_max:", data['main']['temp_max'])
print("conditions:", data['weather'][0]['description'])
