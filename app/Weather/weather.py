from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

#schema for pydantic

class WeatherBase(BaseModel):
    city: str = Field(min_length=3, max_length=20)
    sunrise: datetime
    sunset: datetime
    longitude: float
    latitude: float
    weather: str
    weather_description: str
    icon: str
    temperature: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None
    visibility: Optional[int] = None
    time: datetime
    wind: Dict[str, float] = {'speed': 0.0, 'deg': 0}
    rain: Dict[str, float] = {'1h': 0.0}
    clouds: Dict[str, int] = {'all': 0}

class WeatherResponse(WeatherBase):
    id: int

    class Config:
        orm_mode = True