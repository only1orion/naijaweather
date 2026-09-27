import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

if not OPENWEATHER_API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY is not set in .env")

# OpenWeatherMap
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_UNITS = "metric"

# Cache
CACHE_TTL_SECONDS = 600  # 10 minutes