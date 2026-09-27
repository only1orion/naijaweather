from fastapi import FastAPI, HTTPException, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app import cache
from app.cities import NIGERIAN_CITIES, is_supported_city, normalize_city
from app.weather import fetch_weather

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="NaijaWeather API",
    description="A lightweight weather API for major Nigerian cities. "
                "Powered by OpenWeatherMap.",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


@app.get("/", tags=["General"])
def root():
    """Welcome endpoint with basic info about the API."""
    return {
        "name": "NaijaWeather API",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": {
            "list_cities": "/cities",
            "weather_by_city": "/weather/{city}",
            "health": "/health",
        },
    }


@app.get("/health", tags=["General"])
async def health():
    """Health check — verifies Redis connectivity too."""
    redis_ok = await cache.ping()
    return {
        "status": "ok",
        "redis": "connected" if redis_ok else "unavailable",
    }


@app.get("/cities", tags=["Cities"])
def list_cities():
    """List all supported Nigerian cities."""
    return {
        "count": len(NIGERIAN_CITIES),
        "cities": list(NIGERIAN_CITIES.keys()),
    }


@app.get("/weather/{city}", tags=["Weather"])
@limiter.limit("30/minute")
async def get_weather(request: Request, city: str):
    """
    Get current weather for a Nigerian city.

    Rate limit: 30 requests per minute per IP.
    Example: `/weather/lagos`
    """
    normalized = normalize_city(city)

    if not is_supported_city(normalized):
        raise HTTPException(
            status_code=400,
            detail=f"'{city}' is not a supported Nigerian city. See /cities for the list.",
        )

    query_city = normalized.replace("-", " ")

    return await fetch_weather(query_city)