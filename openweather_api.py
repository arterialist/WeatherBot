from datetime import datetime

from forecast_info import ForecastInfo
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

    def get_next_3_hours(self, latitude, longitude) -> list:
        forecast_data: dict = self.get_request(f"{self.base_url}/onecall", {
            "appid": self.api_key,
            "lat": latitude,
            "lon": longitude,
            "units": "metric",
            "lang": "ru"
        })
        try:
            forecast_data: list = forecast_data.get("hourly")[:3]
        except TypeError:
            return []
        forecast_info_list = []
        for forecast in forecast_data:
            forecast_info = ForecastInfo(
                weather_info=WeatherInfo(
                    weather_state=forecast.get("weather")[0].get("description"),
                    temperature_value=forecast.get("temp"),
                    temperature_unit="C"
                ),
                date_time=datetime.fromtimestamp(forecast.get("dt")).strftime("%H:%M")
            )
            forecast_info_list.append(forecast_info)
        print(forecast_data)
        return forecast_info_list

    def get_tomorrow_forecast(self, latitude, longitude) -> WeatherInfo:
        forecast_data: dict = self.get_request(f"{self.base_url}/onecall", {
            "appid": self.api_key,
            "lat": latitude,
            "lon": longitude,
            "units": "metric",
            "lang": "ru"
        })
        try:
            weather_data: dict = forecast_data.get("daily")[1]
            weather_info: WeatherInfo = WeatherInfo(
                weather_state=weather_data.get("weather")[0].get("description"),
                temperature_value=(weather_data.get("temp").get("min") + weather_data.get("temp").get("max")) / 2.0,
                temperature_unit="C",
                image_url=f"http://openweathermap.org/img/w/{weather_data.get('weather')[0].get('icon')}.png",
            )
            return weather_info
        except TypeError:
            return WeatherInfo("Clear", 0, "C")
