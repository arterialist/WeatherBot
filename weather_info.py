class WeatherInfo:
    def __init__(self, weather_state: str, temperature_value: float, temperature_unit: str, image_url: str = "https://t.me"):
        self.image_url = image_url
        self.temperature_unit = temperature_unit
        self.temperature_value = temperature_value
        self.weather_state = weather_state
