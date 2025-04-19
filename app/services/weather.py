import os
import requests
from datetime import datetime, timedelta
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "3d3497329215abf4be6c899dcb6357e3")
weather_cache = {}


@retry(
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    reraise=True
)
def fetch_weather(zip_code: str):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?zip={zip_code}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


def get_weather_by_zip(zip_code: str):
    now = datetime.utcnow()
    cached = weather_cache.get(zip_code)

    if cached and (now - cached["timestamp"]) < timedelta(hours=2):
        return cached["data"]

    try:
        data = fetch_weather(zip_code)
    except requests.exceptions.RequestException:
        return {"warning": "Weather service unavailable"}

    parsed = {
        "description": data["weather"][0]["description"],
        "temperature": data["main"]["temp"],
        "city": data["name"]
    }

    weather_cache[zip_code] = {
        "data": parsed,
        "timestamp": now
    }

    return parsed
