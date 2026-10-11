import requests

def fetch_weather(city):
    # Example using OpenWeatherMap API
    api_key = "your_api_key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    return response.json()  # or parse specific weather data