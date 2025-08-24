from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.core.database import Base
from datetime import datetime, timezone

class Weather(Base):
    __tablename__ = 'weather_cache'
    
    id = Column(Integer, primary_key=True)
    city = Column(String)
    sunrise = Column(DateTime(timezone=True))
    sunset = Column(DateTime(timezone=True))
    longitude = Column(Float)
    latitude = Column(Float)
    weather = Column(String)
    weather_description = Column(String)
    icon = Column(String)
    temperature = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    humidity = Column(Integer)
    sea_level = Column(Integer)
    grnd_level = Column(Integer)
    visibility = Column(Integer)
    time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    wind = Column(JSON, default={'speed': 0.0, 'deg': 0})
    rain = Column(JSON, default={'1h': 0.0})
    clouds = Column(JSON, default={'all': 0})