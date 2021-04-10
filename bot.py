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

actions = [
    "Текущая погода",
    "Прогноз на 3 часа",
    "Прогноз на завтра"
]


@bot.message_handler(commands=["ping"])
def ping_handler(message: Message):
    bot.send_message(message.chat.id, "Pong")


def handle_provider_reply(message: Message, action: str, latitude, longitude):
    provider = message.text
    print(latitude)
    print(longitude)

    msg_text = "Выбран неизвестный провайдер! Пожалуйста повторите операцию."
    temp_msg = bot.send_message(message.chat.id, f"Запрашиваем информацию от {provider}...")
    if provider == "AccuWeather":
        location_key = accuweather_api.get_location_key(latitude, longitude)
        if action == actions[0]:
            weather_info: WeatherInfo = accuweather_api.get_current_weather(location_key)
            msg_text = f"{action}:\n\n<a href='{weather_info.image_url}'>{weather_info.weather_state}</a>, температура {weather_info.temperature_value:.2f}°{weather_info.temperature_unit}"
        elif action == actions[1]:
            forecast_info_list = accuweather_api.get_next_3_hours(location_key)
            msg_text = f"{action}:\n\n"
            for forecast_info in forecast_info_list:
                weather_info: WeatherInfo = forecast_info.weather_info
                date = forecast_info.date_time
                msg_text += f"<b>{date}</b> - {weather_info.weather_state}, {weather_info.temperature_value:.2f}°{weather_info.temperature_unit}\n\n"
        elif action == actions[2]:
            msg_text = "Not implemented"

    elif provider == "WeatherAPI":
        if action == actions[0]:
            weather_info: WeatherInfo = weatherapi_api.get_current_weather(latitude, longitude)
            msg_text = f"{action}:\n\n<a href='{weather_info.image_url}'>{weather_info.weather_state}</a>, температура {weather_info.temperature_value:.2f}°{weather_info.temperature_unit}"
        elif action == actions[1]:
            msg_text = "Данный провайдер не предоставляет почасовой прогноз, попробуйте другого :("
        elif action == actions[2]:
            weather_info: WeatherInfo = weatherapi_api.get_tomorrow_forecast(latitude, longitude)
            msg_text = f"{action}:\n\n<a href='{weather_info.image_url}'>{weather_info.weather_state}</a>, температура {weather_info.temperature_value:.2f}°{weather_info.temperature_unit}"

    elif provider == "OpenWeather":
        if action == actions[0]:
            weather_info: WeatherInfo = openweather_api.get_current_weather(latitude, longitude)
            msg_text = f"{action}:\n\n<a href='{weather_info.image_url}'>{weather_info.weather_state}</a>, температура {weather_info.temperature_value:.2f}°{weather_info.temperature_unit}"
        elif action == actions[1]:
            forecast_info_list = openweather_api.get_next_3_hours(latitude, longitude)
            msg_text = f"{action}:\n\n"
            for forecast_info in forecast_info_list:
                weather_info: WeatherInfo = forecast_info.weather_info
                date = forecast_info.date_time
                msg_text += f"<b>{date}</b> - {weather_info.weather_state}, {weather_info.temperature_value}°{weather_info.temperature_unit}\n\n"
        elif action == actions[2]:
            weather_info: WeatherInfo = openweather_api.get_tomorrow_forecast(latitude, longitude)
            msg_text = f"П{action}:\n\n<a href='{weather_info.image_url}'>{weather_info.weather_state}</a>, температура {weather_info.temperature_value:.2f}°{weather_info.temperature_unit}"

    bot.delete_message(message.chat.id, temp_msg.message_id)
    bot.send_message(message.chat.id, msg_text, parse_mode="HTML")


def handle_action_reply(message: Message, latitude, longitude):
    action = message.text

    if action not in actions:
        bot.send_message(message.chat.id, "Выбрано неизвестное действие! Пожалуйста повторите операцию.")
        return

    bot_message = bot.send_message(message.chat.id, text="Выберите провайдера из списка.", reply_markup=ForceReply(selective=True))
    bot.register_for_reply(bot_message, lambda x: handle_provider_reply(x, action, latitude, longitude))
    keyboard_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard_markup.add(KeyboardButton("AccuWeather"))
    keyboard_markup.add(KeyboardButton("WeatherAPI"))
    keyboard_markup.add(KeyboardButton("OpenWeather"))
    bot.send_message(message.chat.id, "Данные от разных провайдеров могут отличаться!", reply_markup=keyboard_markup)


@bot.message_handler(content_types=["location"])
def handle_location(message: Message):
    location: Location = message.location
    latitude = location.latitude
    longitude = location.longitude
    bot_message = bot.send_message(message.chat.id, text="Что будем делать?", reply_markup=ForceReply(selective=True))
    bot.register_for_reply(bot_message, lambda x: handle_action_reply(x, latitude, longitude))
    keyboard_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard_markup.add(KeyboardButton("Текущая погода"))
    keyboard_markup.add(KeyboardButton("Прогноз на 3 часа"))
    keyboard_markup.add(KeyboardButton("Прогноз на завтра"))
    bot.send_message(message.chat.id, "Выберите одно из действий на клавиатуре:", reply_markup=keyboard_markup)


if __name__ == "__main__":
    bot.polling(True)
