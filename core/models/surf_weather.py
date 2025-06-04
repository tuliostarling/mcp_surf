from pydantic import BaseModel
from typing import Optional


class SurfWeatherInput(BaseModel):
    location: str
    date: Optional[str] = None
