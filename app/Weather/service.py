from sqlalchemy.ext.asyncio import AsyncSession
from app.Weather.repository import get_weather, create_weather, upsert_weather
from app.Weather.weatherapi import OpenWeather
from fastapi import Depends
import datetime
from app.core.database import get_db
import httpx

async def fetch_weather(city: str, db: AsyncSession):
	ow = OpenWeather()
	try:
		data = await ow.get_data("weather", city)
	except httpx.HTTPStatusError as e:
		if e.response.status_code == 404:
			return {"detail": f"City '{city}' not found!"}
		else:
			raise e
	
	weather_data = {
		"city": city,
		"sunrise": datetime.datetime.fromtimestamp(data["sys"]["sunrise"], tz=datetime.timezone.utc),
		"sunset": datetime.datetime.fromtimestamp(data["sys"]["sunset"], tz=datetime.timezone.utc),
		"longitude": data["coord"]["lon"],
		"latitude": data["coord"]["lat"],
		"weather": data["weather"][0]["main"],
		"weather_description": data["weather"][0]["description"],
		"icon": data["weather"][0]["icon"],
		"temperature": data["main"]["temp"],
		"feels_like": data["main"]["feels_like"],
		"temp_min": data["main"]["temp_min"],
		"temp_max": data["main"]["temp_max"],
		"pressure": data["main"]["pressure"],
		"humidity": data["main"]["humidity"],
		"sea_level": data["main"]["sea_level"],
		"grnd_level": data["main"]["grnd_level"],
		"visibility": data["visibility"],
		"time": datetime.datetime.fromtimestamp(data["dt"], tz=datetime.timezone.utc),
		"wind": data.get("wind", {"speed": 0.0, "deg": 0}),
		"rain": data.get("rain", {"1h": 0.0}),
		"clouds": data.get("clouds", {"all": 0})
	}
	
	ext = await get_weather(db, city)
	if ext:
		weather = await upsert_weather(db, city, weather_data)
	else:
		weather = await create_weather(db, weather_data)
	
	return weather
