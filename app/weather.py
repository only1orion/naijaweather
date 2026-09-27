import httpx
from fastapi import HTTPException

from app import cache, config


async def fetch_weather(city: str, units: str = "metric") -> dict:
    """
    Fetch current weather for a Nigerian city.
    Uses Redis cache with TTL to avoid hammering OpenWeatherMap.
    """
    cache_key = f"weather:{units}:{city.lower().replace(' ', '-')}"

    # 1. Try cache first
    cached = await cache.get_cached(cache_key)
    if cached is not None:
        cached["cached"] = True
        return cached

    # 2. Cache miss — hit OpenWeatherMap
    params = {
        "q": f"{city},NG",
        "appid": config.OPENWEATHER_API_KEY,
        "units": units,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(config.OPENWEATHER_BASE_URL, params=params)
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Upstream error: {exc}")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"City '{city}' not found")
    if response.status_code == 401:
        raise HTTPException(status_code=500, detail="Invalid API key")
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"OpenWeatherMap returned {response.status_code}",
        )

    raw = response.json()

    payload = {
        "city": raw["name"],
        "country": raw["sys"]["country"],
        "coordinates": {
            "lat": raw["coord"]["lat"],
            "lon": raw["coord"]["lon"],
        },
        "temperature": {
            "current": raw["main"]["temp"],
            "feels_like": raw["main"]["feels_like"],
            "min": raw["main"]["temp_min"],
            "max": raw["main"]["temp_max"],
        },
        "humidity": raw["main"]["humidity"],
        "pressure": raw["main"]["pressure"],
        "wind": {
            "speed": raw["wind"]["speed"],
            "direction": raw["wind"].get("deg"),
        },
        "condition": {
            "main": raw["weather"][0]["main"],
            "description": raw["weather"][0]["description"],
            "icon": raw["weather"][0]["icon"],
        },
        "units": units,
        "cached": False,
    }

    # 3. Store in cache for next time
    await cache.set_cached(cache_key, payload)

    return payload