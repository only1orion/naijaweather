# 🌦️ NaijaWeather API

A lightweight FastAPI service that aggregates real-time weather data for major Nigerian cities, powered by OpenWeatherMap.

Built with caching, rate limiting, and clean auto-generated documentation.

## Features

- 🌍 **12+ Nigerian cities** supported out of the box
- ⚡ **Redis caching** (10-min TTL) — dramatically reduces upstream API calls
- 🛡️ **Rate limiting** — 30 requests/minute per IP
- 📖 **Interactive docs** — Swagger UI at `/docs`, ReDoc at `/redoc`
- 🧩 **Clean response shape** — our own format, not raw OpenWeatherMap
- 🩺 **Health check** endpoint with Redis status
- 🐳 **Docker-ready**

## Tech Stack

- **FastAPI** — async web framework
- **httpx** — async HTTP client
- **Redis (Memurai on Windows)** — caching layer
- **slowapi** — rate limiting
- **OpenWeatherMap API** — weather data source
- **Uvicorn** — ASGI server

## Quick Start

### 1. Clone & install

```bash
git clone <your-repo-url>
cd naijaweather
python -m venv venv
venv\Scripts\activate         # Windows
# source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```
OPENWEATHER_API_KEY=your_key_here
REDIS_URL=redis://localhost:6379
```

Get a free API key at [openweathermap.org](https://openweathermap.org/api).

### 3. Start Redis

**Docker (recommended):**
```bash
docker run -d --name naijaweather-redis -p 6379:6379 redis:7-alpine
```

**Windows without Docker:** install [Memurai](https://www.memurai.com/get-memurai).

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Visit **http://localhost:8000/docs** for interactive documentation.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome info |
| GET | `/health` | Health check (includes Redis status) |
| GET | `/cities` | List all supported Nigerian cities |
| GET | `/weather/{city}` | Current weather for a city |

### Example

```bash
curl http://localhost:8000/weather/lagos
```

```json
{
  "city": "Lagos",
  "country": "NG",
  "temperature": {
    "current": 27.29,
    "feels_like": 30.97
  },
  "humidity": 85,
  "condition": {
    "main": "Clouds",
    "description": "overcast clouds"
  },
  "cached": false
}
```

The `cached` field tells you whether the response came from Redis (`true`) or a fresh upstream call (`false`).

## Supported Cities

Lagos, Abuja, Kano, Ibadan, Port Harcourt, Benin City, Kaduna, Enugu, Aba, Jos, Ilorin, Maiduguri

## Project Structure

```
naijaweather/
├── app/
│   ├── main.py       # FastAPI app + endpoints
│   ├── config.py     # Env vars & constants
│   ├── cities.py     # Supported Nigerian cities
│   ├── cache.py      # Redis helpers
│   └── weather.py    # OpenWeatherMap client + reshaping
├── requirements.txt
├── .env              # (gitignored)
└── README.md
```

## Rate Limits

- **30 requests / minute / IP** on `/weather/{city}`
- Exceeding returns `429 Too Many Requests`

## License

MIT