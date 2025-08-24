import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_wether_valid():
    async with AsyncClient(app=app, base_url="https://test") as ac:
        await ac.post("/weather/add", data = {"q": "Kyiv"})
        response = await ac.get("/weather/Kyiv")
    assert response.status_code == 200
    assert "Kyiv" in response.text

@pytest.mark.asyncio
async def test_get_wether_invalid():
    async with AsyncClient(app=app, base_url="https://test") as ac:
        response = await ac.get("/weather/InvalidCity123")
    assert response.status_code == 404 or "detail" in response.json()
    
@pytest.mark.asyncio
async def test_add_weather_valid():
    async with AsyncClient(app=app, base_url="https://test") as ac:
        response = await ac.post("/weather/add", data={"q": "Kyiv"})
    assert response.status_code == 303
    
@pytest.mark.asyncio
async def test_add_weather_empty():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/weather/add", data={"q": ""})
    assert response.status_code == 200
    assert "City is required" in response.text
    
@pytest.mark.asyncio
async def test_delete_weather():
    async with AsyncClient(app=app, base_url="https://test") as ac:
        await ac.post("/weather/add", data={"q": ""})
        response = await ac.post("/weather/delete/Kyiv")
        
    assert response.status_code == 303
    assert response.headers["location"] == "/weather/"
    
    async with AsyncClient(app=app, base_url="https://test") as ac:
        response = await ac.get("/weather/Kyiv")
    assert response.status_code == 404
