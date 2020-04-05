import os

from telebot import TeleBot
from telebot.types import Message, Location, ForceReply, ReplyKeyboardMarkup, KeyboardButton

from accuweather_api import AccuWeatherAPI
from openweather_api import OpenWeatherAPI
from weather_info import WeatherInfo
from weatherapi_api import WeatherAPI

TOKEN = os.getenv("WEATHER_BOT_TOKEN")
ACCUWEATHER_TOKEN = os.getenv("ACCUWEATHER_TOKEN")
WEATHERAPI_TOKEN = os.getenv("WEATHERAPI_TOKEN")
OPENWEATHER_TOKEN = os.getenv("OPENWEATHER_TOKEN")

accuweather_api = AccuWeatherAPI(ACCUWEATHER_TOKEN)
weatherapi_api = WeatherAPI(WEATHERAPI_TOKEN)
openweather_api = OpenWeatherAPI(OPENWEATHER_TOKEN)
bot = TeleBot(TOKEN, skip_pending=True)


@bot.message_handler(commands=["ping"])
def ping_handler(message: Message):
    bot.send_message(message.chat.id, "Pong")


def handle_provider_reply(message: Message, latitude, longitude):
    provider = message.text
    print(latitude)
    print(longitude)

    msg_text = "Выбран неизвестный провайдер! Пожалуйста повторите операцию."
    temp_msg = bot.send_message(message.chat.id, f"Запрашиваем информацию от {provider}...")
    if provider == "AccuWeather":
        location_key = accuweather_api.get_location_key(latitude, longitude)
        weather_info: WeatherInfo = accuweather_api.get_current_weather(location_key)
        msg_text = f"Погода в выбранной локации:\n<a href='{weather_info.image_url}'>{weather_info.weather_state}</a>, температура {weather_info.temperature_value}°{weather_info.temperature_unit}"
    elif provider == "WeatherAPI":
        weather_info: WeatherInfo = weatherapi_api.get_current_weather(latitude, longitude)
        msg_text = f"Погода в выбранной локации:\n<a href='{weather_info.image_url}'>{weather_info.weather_state}</a>, температура {weather_info.temperature_value}°{weather_info.temperature_unit}"
    elif provider == "OpenWeather":
        weather_info: WeatherInfo = openweather_api.get_current_weather(latitude, longitude)
        msg_text = f"Погода в выбранной локации:\n<a href='{weather_info.image_url}'>{weather_info.weather_state}</a>, температура {weather_info.temperature_value}°{weather_info.temperature_unit}"

    bot.delete_message(message.chat.id, temp_msg.message_id)
    bot.send_message(message.chat.id, msg_text, parse_mode="HTML")


@bot.message_handler(content_types=["location"])
def handle_location(message: Message):
    location: Location = message.location
    latitude = location.latitude
    longitude = location.longitude
    bot_message = bot.send_message(message.chat.id, text="Выберите поставщика погоды:", reply_markup=ForceReply(selective=True))
    bot.register_for_reply(bot_message, lambda x: handle_provider_reply(x, latitude, longitude))
    keyboard_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard_markup.add(KeyboardButton("AccuWeather"))
    keyboard_markup.add(KeyboardButton("WeatherAPI"))
    keyboard_markup.add(KeyboardButton("OpenWeather"))
    bot.send_message(message.chat.id, "Данные от разных поставщиков могут различаться!", reply_markup=keyboard_markup)


if __name__ == "__main__":
    bot.polling(True)
