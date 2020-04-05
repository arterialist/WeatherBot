from generic_api import APIInterface
from weather_info import WeatherInfo


class AccuWeatherAPI(APIInterface):
    base_url: str = "https://dataservice.accuweather.com"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_location_key(self, latitude: str, longitude: str) -> str:
        location_key = self.get_request(f"{self.base_url}/locations/v1/cities/geoposition/search", {
            "apikey": self.api_key,
            "q": f"{latitude},{longitude}",
            "language": "ru-ru"
        })
        return location_key.get("Key")

    def get_current_weather(self, location_key: str) -> WeatherInfo:
        try:
            weather_data: dict = self.get_request(f"{self.base_url}/currentconditions/v1/{location_key}", {
                "apikey": self.api_key,
                "language": "ru-ru"
            })
            weather_data = weather_data[0]
        except KeyError as e:
            return WeatherInfo("Clear", 0, "C")

        weather_info = WeatherInfo(
            weather_state=weather_data.get("WeatherText"),
            temperature_value=weather_data.get("Temperature").get("Metric").get("Value"),
            temperature_unit=weather_data.get("Temperature").get("Metric").get("Unit"),
            image_url=f"https://developer.accuweather.com/sites/default/files/{str(weather_data.get('WeatherIcon')).zfill(2)}-s.png"
        )
        return weather_info
