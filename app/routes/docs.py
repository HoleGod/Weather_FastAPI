from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.Weather.models import Weather
from app.Weather.weather import WeatherBase, WeatherResponse
from app.Weather.service import fetch_weather
from app.core.database import get_db
from sqlalchemy.future import select
from app.Weather.repository import delete_weather

router = APIRouter(
    prefix="/weather_docs",
    tags=["weather"],
)

@router.get("/", response_model=List[WeatherResponse])
async def get_all_weather(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Weather))
    weather_list = result.scalars().all()
    return weather_list

@router.get("/{city}", response_model=WeatherBase)
async def get_weather_by_city(city: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Weather).where(Weather.city == city))
    weather = result.scalars().first()
    if not weather:
        raise HTTPException(status_code=404, detail="Weather info not found!")
    return weather

@router.post("/api/{city}", response_model=WeatherBase)
async def get_weather_from_api(city: str, db: AsyncSession = Depends(get_db)):
    dbr = await fetch_weather(city, db)
    
    return dbr

@router.delete("/{city}")
async def delete_weather_by_city(city: str, db: AsyncSession = Depends(get_db)):
    await delete_weather(db, city)
    return {"detail": f"Weather info for city '{city}' deleted"}
