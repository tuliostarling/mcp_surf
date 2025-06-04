from mcp.server.fastmcp import FastMCP
from services.mcp.functions import fetch_surf_data, fetch_weather_data


def get_app() -> FastMCP:
    mcp = FastMCP("Surf-Weather-Tools")

    @mcp.tool(
        name="get_surf_data",
        description="Return surf conditions (wave height, swell, water temp, …) for a beach and date. "
        "Use when the user asks about waves, swell, water temp, tides, or surf quality.",
    )
    async def get_surf_data(location: str, date: str):
        return await fetch_surf_data(location, date)

    @mcp.tool(
        name="get_weather_data",
        description="Return weather forecast (temp, wind, rain, …) for a place and date. "
        "Use when the user asks about weather, climate, or outdoor conditions not specific to surfing.",
    )
    async def get_weather_data(location: str, date: str | None = None):
        return await fetch_weather_data(location, date)

    return mcp.streamable_http_app()
