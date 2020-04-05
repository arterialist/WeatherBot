from weather_info import WeatherInfo


class ForecastInfo:
    def __init__(self, weather_info: WeatherInfo, date_time: str):
        self.weather_info = weather_info
        self.date_time = date_time
