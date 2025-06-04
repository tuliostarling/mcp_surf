import asyncio
from typing import List
from langchain_community.tools import StructuredTool
from mcp import ClientSession
from mcp.types import Tool
from mcp.client.streamable_http import streamablehttp_client
from core.models.surf_weather import SurfWeatherInput

MCP_ENDPOINT = "http://localhost:9000/mcp"


class MCPToolAdapter:
    def __init__(self, base_url: str = MCP_ENDPOINT):
        self.base_url = base_url
        self._tools: List[StructuredTool] | None = None
        self._lock = asyncio.Lock()

    async def load(self) -> List[StructuredTool]:
        if self._tools:
            return self._tools

        async with self._lock:
            if self._tools:
                return self._tools
            catalogue = await self._catalogue()

            tools_entry = next((item for item in catalogue if item[0] == "tools"), None)
            tool_defs = tools_entry[1] if tools_entry else []

            self._tools = [
                self._wrap(tool)
                for tool in tool_defs
                if tool.name not in ("meta", "nextCursor")
            ]
            return self._tools

    async def _catalogue(self) -> List:
        """Fetch the tool list from the MCP server."""
        async with streamablehttp_client(self.base_url) as (read_s, write_s, _c):
            async with ClientSession(read_s, write_s) as session:
                await session.initialize()
                return await session.list_tools()

    def _wrap(self, tool: Tool) -> StructuredTool:
        """Convert an mcp tool object into a langchain structuredtool."""

        async def _async_caller(**kwargs):
            async with streamablehttp_client(self.base_url) as (read_s, write_s, _c):
                async with ClientSession(read_s, write_s) as session:
                    await session.initialize()
                    return await session.call_tool(tool.name, kwargs)

        def _sync_wrapper(**kwargs):
            try:
                return asyncio.run(_async_caller(**kwargs))
            except RuntimeError:
                return asyncio.get_event_loop().run_until_complete(
                    _async_caller(**kwargs)
                )

        _sync_wrapper.__name__ = tool.name
        _sync_wrapper.__doc__ = tool.description or f"Call MCP tool `{tool.name}`"

        return StructuredTool.from_function(
            func=_sync_wrapper,
            name=tool.name,
            description=tool.description,
            args_schema=SurfWeatherInput,
        )
