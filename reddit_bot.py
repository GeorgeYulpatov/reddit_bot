# Импортирую библиотеку для работы с асинхронными функциями так как библиотека
# Aiogram является синхронной
import asyncio
# Импортирую фаил config, в котором храниться словарь с требуемыми ID
import config
# Импортирую библиотеку для Reddit API (Для этого шага регистрировались на Reddit, что бы получить
# CLIENT_ID и SECRET_CODE.)
import asyncpraw
# Импортирую библиотеку для работы c Telegram.
from aiogram import Bot, types

# Обращаюсь к файлу config,для того чтобы задать значение переменной( после этой строчки кода
# import config начинает подсвечиватся)
API_TOKEN = config.settings['TOKEN']
# ID созданого канала Telegram
CHANNEL_ID = -1001801092692

# Создаем бота, заполняем аргументы. То есть задаем клиент связи с ботом в телеграм(начинает светиться подтягивание
# библиотеки для работы с телеграм aiogram)
bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
# Создаем обьект reddit с использованием библиотеки asyncpraw
reddit = asyncpraw.Reddit(client_id=config.settings['CLIENT_ID'],
                          client_secret=config.settings['SECRET_CODE'],
                          user_agent='test_random_radit_bot/0.0.1')

mems = []  # Каждый отправленый мем будет записываться в список, что бы исключить повторения
TIMEOUT = 5  # Переодичность времени обращения к Raddit выраженная в секундах
SUBREDDIT_NAME = 'memes'  # Имя SUBREDDIT к которому будет обращение https://www.reddit.com/r/memes/
POST_LIMIT = 1  # Количество записей, то есть одну последнею запись


# Функция(асинхронная) для
async def send_massage(channel_id: int, text: str):
    await bot.send_message(channel_id, text)  # Обращение к боту в строке 20 и говорим ему
    # отправь сообщение сообщаем текст и ID канала в телеграм


# Также функция(асинхронная)
async def main():
    while True:  # Запуск безконечного цикла
        await asyncio.sleep(TIMEOUT)  # Пауза между постами равная значению переменной, условный сон
        memes_submissions = await reddit.subreddit(SUBREDDIT_NAME)  # SUBREDDIT к которому будет обращение
        memes_submissions = memes_submissions.new(
            limit=POST_LIMIT)  # Получение самого нового поста, с ограничением количества постов
        item = await memes_submissions.__anext__()  # memes_submissions  проевратился в асинхронный генератор,
        # обращаемся через a
        if item.title not in mems:
            mems.append(item.title)  # Добавление заголовка в список для последующей сверки со списком контента
            await send_massage(CHANNEL_ID, item.url)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# https://www.youtube.com/watch?v=oAKVM7h4Kp4&t=147s
