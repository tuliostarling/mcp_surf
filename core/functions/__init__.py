from langchain.tools import tool
from core.functions.surf import fetch_surf_data
from core.functions.weather import fetch_weather_data


@tool(
    name_or_callable="get_surf_data",
    description=(
        "Return surf conditions (wave height, swell, water temp, …) for a beach and date."
        "Use when the user asks about waves, swell, water temp, tides, or surf quality."
    ),
)
async def get_surf_data(location: str, date: str):
    return await fetch_surf_data(location, date)


@tool(
    name_or_callable="get_weather_data",
    description=(
        "Return weather forecast (temp, wind, rain, …) for a place and date."
        "Use when the user asks about weather, climate, or outdoor conditions not specific to surfing."
    ),
)
async def get_weather_data(location: str, date: str | None = None):
    return await fetch_weather_data(location, date)


functions = [get_surf_data, get_weather_data]
