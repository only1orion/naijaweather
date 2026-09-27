import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise SystemExit("❌ OPENWEATHER_API_KEY missing from .env")

CITY = "Lagos"

url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": f"{CITY},NG",
    "appid": API_KEY,
    "units": "metric",
}

print(f"Fetching weather for {CITY}...\n")

response = httpx.get(url, params=params, timeout=10)
print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print(f"City:        {data['name']}")
    print(f"Temp:        {data['main']['temp']}°C")
    print(f"Feels like:  {data['main']['feels_like']}°C")
    print(f"Condition:   {data['weather'][0]['description']}")
    print(f"Humidity:    {data['main']['humidity']}%")
    print(f"Wind speed:  {data['wind']['speed']} m/s")
else:
    print("Error body:", response.text)