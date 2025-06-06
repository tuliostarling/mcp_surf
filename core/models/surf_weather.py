from langchain_core.pydantic_v1 import BaseModel
from typing import Optional


class SurfWeatherInput(BaseModel):
    location: str
    date: Optional[str] = None
