import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

import requests
from config import TOKEN


API_KEY = '272009fd696656bbaea88b8d974dd950'  # Замените на ваш ключ API
# TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Замените на токен вашего бота
CITY = 'Тюмень'  # Укажите город


# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Создание экземпляра бота и диспетчера
# bot = Bot(token=TOKEN)
dp = Dispatcher()


async def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        return f"Прогноз погоды для {city}:\nТемпература: {temperature}°C\nОписание: {weather_description.capitalize()}"
    else:
        return "Не удалось получить данные о погоде."


@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот, который предоставляет прогноз погоды. Напиши /weather, чтобы получить прогноз погоды.")


@dp.message(Command('weather'))
async def cmd_weather(message: Message):
    weather_info = await get_weather(CITY)
    await message.answer(weather_info, parse_mode=ParseMode.MARKDOWN)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
