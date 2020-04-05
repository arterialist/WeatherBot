from generic_api import APIInterface
from weather_info import WeatherInfo


class OpenWeatherAPI(APIInterface):
    base_url: str = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_current_weather(self, latitude, longitude) -> WeatherInfo:
        weather_data: dict = self.get_request(f"{self.base_url}/weather", {
            "appid": self.api_key,
            "lat": latitude,
            "lon": longitude,
            "units": "metric",
            "lang": "ru"
        })
        weather_info: WeatherInfo = WeatherInfo(
            weather_state=weather_data.get("weather")[0].get("description"),
            temperature_value=weather_data.get("main").get("temp"),
            temperature_unit="C",
            image_url=f"http://openweathermap.org/img/w/{weather_data.get('weather')[0].get('icon')}.png",
        )
        return weather_info
