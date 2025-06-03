import httpx
from config import AppSettings

WEATHERAPI_KEY = AppSettings().weather_api_key


async def fetch_surf_data(location: str, date: str) -> dict:
    weatherapi_url = "http://api.weatherapi.com/v1/marine.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": location,
        "dt": date,
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(weatherapi_url, params=params)
        response_json = res.json()
        forecast_day = response_json["forecast"]["forecastday"][0]
        data = forecast_day["hour"][0]

    tides = forecast_day.get("day", {}).get("tides", [{}])[0].get("tide", [])

    return {
        "waveHeight": data.get("sig_ht_mt", "Unknown"),
        "swellHeight": data.get("swell_ht_mt", "Unknown"),
        "swellDirection": data.get("swell_dir_16_point", "Unknown"),
        "swellPeriod": data.get("swell_period_secs", "Unknown"),
        "waterTemperature": data.get("water_temp_c", "Unknown"),
        "windSpeed": data.get("wind_kph", "Unknown"),
        "windDirection": data.get("wind_dir", "Unknown"),
        "tides": tides,
        "condition": data.get("condition", {}).get("text", "Unknown"),
        "time": data.get("time", "Unknown"),
    }
