import httpx
from config.settings import AppSettings

WEATHERAPI_KEY = AppSettings().weather_api_key


async def fetch_weather_data(location: str, date: str = None) -> dict:
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": location,
        "days": 7,
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        forecast_days = res.json()["forecast"]["forecastday"]

    forecast_for_date = next(
        (day for day in forecast_days if day["date"] == date), None
    )

    if not forecast_for_date:
        return {"error": f"No forecast data available for {date}"}

    day_data = forecast_for_date["day"]
    return {
        "forecast": day_data["condition"]["text"],
        "temp": day_data["avgtemp_c"],
        "wind": day_data["maxwind_kph"],
        "precip": day_data["totalprecip_mm"],
        "humidity": day_data["avghumidity"],
        "uv_index": day_data["uv"],
    }
