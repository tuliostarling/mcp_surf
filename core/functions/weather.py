import httpx
from config.settings import AppSettings

WEATHERAPI_KEY = AppSettings().weather_api_key


async def fetch_weather_data(location: str, date: str | None = None) -> dict:
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {"key": WEATHERAPI_KEY, "q": location, "days": 7}

    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        forecast_days = res.json()["forecast"]["forecastday"]

    target_date = date or forecast_days[0]["date"]
    day = next((d for d in forecast_days if d["date"] == target_date), None)

    if not day:
        day = forecast_days[0]

    day_data = day["day"]
    return {
        "date": target_date,
        "forecast": day_data["condition"]["text"],
        "temp": day_data["avgtemp_c"],
        "wind": day_data["maxwind_kph"],
        "precip": day_data["totalprecip_mm"],
        "humidity": day_data["avghumidity"],
        "uv_index": day_data["uv"],
    }
