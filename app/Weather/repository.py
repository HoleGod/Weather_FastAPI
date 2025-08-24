from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Weather
from sqlalchemy import delete
from fastapi import HTTPException

async def get_weather(db: AsyncSession, city: str):
    result = await db.execute(select(Weather).filter_by(city=city))
    return result.scalars().first()

async def create_weather(db: AsyncSession, weather_data: dict):
    weather = Weather(**weather_data)
    db.add(weather)
    await db.commit()
    await db.refresh(weather)
    return weather

async def delete_weather(db: AsyncSession, city: str):
    smt = delete(Weather).where(Weather.city == city)
    res = await db.execute(smt)
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Weather info not found!")
    await db.commit()

async def upsert_weather(db: AsyncSession, city: str, weather_data: dict):
	result = await db.execute(select(Weather).where(Weather.city == city))
	existing = result.scalars().first()

	if existing:
		for key, value in weather_data.items():
			setattr(existing, key, value)
		await db.commit()
		await db.refresh(existing)
		return existing
	else:
		new_weather = Weather(**weather_data)
		db.add(new_weather)
		await db.commit()
		await db.refresh(new_weather)
		return new_weather
