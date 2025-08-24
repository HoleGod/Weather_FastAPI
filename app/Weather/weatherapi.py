from app.core.config import SECRET_KEY
import requests
import httpx
from app.Weather.models import Weather

city_name = "Kyiv"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={SECRET_KEY}&units=metric"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print(data)
    
class OpenWeather:
    def __init__(self, base_url: str = "http://api.openweathermap.org/data/2.5"):
        self.base_url = base_url
        self.api_key = SECRET_KEY
        
    async def get_data(self, endpoint: str, city: str) -> dict:
        url = f"{self.base_url}/{endpoint}"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()