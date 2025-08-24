from fastapi import APIRouter, Request, Depends, HTTPException, Query, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from app.Weather.models import Weather
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Annotated
from app.Weather.service import fetch_weather
from app.Weather.repository import delete_weather

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse) 
async def get_weather(request: Request, db: AsyncSession = Depends(get_db)):
    info = await db.execute(select(Weather))
    weatherlist = info.scalars().all()
        
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "weatherlist": weatherlist}
    )
    
@router.get("/{city}", name="weather_info", response_class=HTMLResponse)
async def weather_info(city: str, request: Request, db: AsyncSession = Depends(get_db)):
    info = await db.execute(select(Weather).where(Weather.city == city))
    weather = info.scalars().first()
    
    if not weather:
        raise HTTPException(status_code=404, detail=f"Weather for '{city}' not found")
    
    return templates.TemplateResponse("detail.html", {"request": request, "weather": weather})

@router.post("/delete/{city}", name="weather_delete")
async def weather_delete(city: str, db: AsyncSession = Depends(get_db)):
    await delete_weather(db, city)
    return RedirectResponse(url="/weather/", status_code=303)

@router.post("/add", name="weather_add")
async def weather_add(q: Annotated[str, Form()] = None, db: AsyncSession = Depends(get_db)):
    if not q:
        return {"detail": "City is required!"}
    weather = await fetch_weather(q, db)

    return RedirectResponse(url="/weather/", status_code=303)