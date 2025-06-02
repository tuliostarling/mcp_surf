from core.functions.surf import fetch_surf_data
from core.functions.weather import fetch_weather_data

function_registry = {
    "get_surf_data": {
        "func": fetch_surf_data,
        "description": "Provides surf conditions including wave height, water temperature, and swell direction.",
    },
    "get_weather_data": {
        "func": fetch_weather_data,
        "description": "Provides weather forecast including temperature, wind, and general conditions.",
    },
}
