import inspect, asyncio
from typing import List, Dict, Any
from langchain_community.tools import StructuredTool
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

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
            self._tools = [self._wrap(meta) for meta in catalogue]
            return self._tools

    async def _catalogue(self) -> List[Dict[str, Any]]:
        """Fetch fresh tool list (one http round-trip)."""
        async with streamablehttp_client(self.base_url) as (read_s, write_s, _c):
            async with ClientSession(read_s, write_s) as session:
                await session.initialize()
                return await session.list_tools()

    def _wrap(self, tool_obj) -> StructuredTool:
        """Convert an mcp tool object into a langchain structuredtool."""
        name = getattr(tool_obj, "name", tool_obj[0])
        desc = getattr(tool_obj, "description", None) or f"MCP tool '{name}'"

        async def _caller(**kwargs):
            async with streamablehttp_client(self.base_url) as (read_s, write_s, _c):
                async with ClientSession(read_s, write_s) as sess:
                    await sess.initialize()
                    return await sess.call_tool(name, kwargs)

        _caller.__name__ = name
        _caller.__doc__ = desc
        _caller.__signature__ = inspect.signature(lambda **kw: None)

        return StructuredTool.from_function(_caller, description=desc)
