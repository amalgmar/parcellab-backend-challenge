"""Weather service for retrieving and caching weather information."""

import os
from datetime import datetime, timedelta
from typing import Dict, Any

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

OPENWEATHER_API_KEY = os.getenv(
    'OPENWEATHER_API_KEY', '3d3497329215abf4be6c899dcb6357e3'
)
weather_cache: Dict[str, Any] = {}


@retry(
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    reraise=True,
)
def fetch_weather(zip_code: str) -> Dict[str, Any]:
    """Fetches weather data from OpenWeatherMap API using a ZIP code.

    This function makes an HTTP GET request to the OpenWeatherMap API to retrieve
    current weather data for the specified ZIP code. It retries on network-related
    errors (e.g., connection timeout, DNS failure) using exponential backoff.

    Retries:
        - Retries up to 3 times on `requests.exceptions.RequestException`
        - Waits exponentially between attempts (min=2s, max=10s)

    Args:
        zip_code (str): The ZIP code for which to fetch weather data.

    Returns:
        dict: Parsed JSON response containing weather information.

    Raises:
        requests.exceptions.RequestException: If all retry attempts fail or if
        a non-200 response is received.
    """
    url = (
        f'https://api.openweathermap.org/data/2.5/weather'
        f'?zip={zip_code}&appid={OPENWEATHER_API_KEY}&units=metric'
    )
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


def get_weather_by_zip(zip_code: str) -> Dict[str, Any]:
    """Gets cached or freshly fetched weather data for a given ZIP code.

    If the data for the given ZIP code is already in the cache, returns it directly.
    Otherwise, fetches it from the external weather API and caches it.

    Args:
        zip_code (str): ZIP code for which to retrieve weather data.

    Returns:
        Dict[str, Any]: A dictionary containing weather details or an error message.
    """
    now = datetime.utcnow()
    cached = weather_cache.get(zip_code)

    if cached and (now - cached['timestamp']) < timedelta(hours=2):
        return cached['data']

    try:
        data = fetch_weather(zip_code)
    except requests.exceptions.RequestException:
        return {'warning': 'Weather service unavailable'}

    parsed = {
        'description': data['weather'][0]['description'],
        'temperature': data['main']['temp'],
        'city': data['name'],
    }

    weather_cache[zip_code] = {'data': parsed, 'timestamp': now}

    return parsed
