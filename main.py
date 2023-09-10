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
        articles[i].print()

        formatted_message = (
            f"*** {articles[i].header} *** \n\n\n"
            f"{articles[i].text} \n\n"
            "[Самые свежие новости тут](https://t.me/wb_articul_channel)"
        )

        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Опубликовать", callback_data=str(len(formatted_message)))
        markup.add(button1)

        await bot.send_message(message.chat.id,
                               formatted_message,
                               parse_mode="Markdown",
                               reply_markup=markup)


# Обработчик команды /mainpage
@dp.message_handler(commands=['mainpage'])
async def on_mainpage(message: types.Message):
    await message.answer('Парсинг главной страницы')


@dp.callback_query_handler(lambda call: call.data.isdigit())
async def send_message(call: types.CallbackQuery):
    global update_text  # Предполагается, что update_text уже объявлен где-то в вашем коде
    message_index = int(call.data)
    if message_index < len(update_text):
        news = update_text[message_index]
        formatted_message = (
            f"*** {news['Заголовок']} *** \n\n\n"
            f"{news['Описание']}\n\n"
            "[Самые свежие новости тут](https://t.me/wb_articul_channel)"
        )
        await bot.send_message(call.from_user.id, formatted_message, parse_mode="Markdown")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
