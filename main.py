import logging
import requests
from bs4 import BeautifulSoup
from article import Article

import aiogram
from aiogram import Bot, Dispatcher, types

API_TOKEN = '6126747598:AAFfM1GS1CC96FPc4hUHLlGYoiszU6ck-zU'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer('Успешно!')


# Обработчик команды /newspage
@dp.message_handler(commands=['newspage'])
async def on_newspage(message: types.Message):
    await message.answer('Парсинг новостной страницы...')
    url = "https://rg.ru/news.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_="ItemOfListStandard_datetime__1tmwG")
    articles = []

    for i in range(len(links)):
        articles.append(Article(links[i]["href"]))
        articles[i].get_info()

    print(articles)



# Обработчик команды /mainpage
@dp.message_handler(commands=['mainpage'])
async def on_mainpage(message: types.Message):
    await message.answer('Парсинг главной страницы')


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
