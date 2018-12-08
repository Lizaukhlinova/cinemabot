from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from mail.query import find_top_five_by_name, list_of_films
from mail.film_page import set_film_info
from mail import common
import requests

from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token='663290175:AAGT2h1895I-xZ_7Ma2VsqcyrQDa2ecV7p8')
dp = Dispatcher(bot, storage=MemoryStorage())


CHOICES = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: 'Ничего не подходит'}


buttons = [KeyboardButton('1'),
           KeyboardButton('2'),
           KeyboardButton('3'),
           KeyboardButton('4'),
           KeyboardButton('5'),
           KeyboardButton('6')]
button_no = KeyboardButton('Ничего не подходит')


class FilmStates(Helper):
    mode = HelperMode.snake_case
    FILM_STATE_0 = ListItem()
    FILM_STATE_1 = ListItem()


LAST_SEARCH_FOR_USER = {}


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.reply("Ура, я супер!")
    await state.set_state(FilmStates.FILM_STATE_0)


@dp.message_handler(state=FilmStates.FILM_STATE_1)
async def choose_film(message: types.Message):
    if message.text not in CHOICES.values():
        await bot.send_message(message.from_user.id,
                               "Поищем другой фильм? Пиши название!")
    elif message.text == CHOICES[6]:
        await bot.send_message(message.from_user.id,
                               "Попробуй уточнить название для более "
                               "качественного поиска.")
    else:
        button = int(message.text)
        films = LAST_SEARCH_FOR_USER[message.from_user.id]
        if button > len(films[common.film_types[0]]):
            button -= len(films[common.film_types[0]])
            films = films[common.film_types[1]]
        else:
            films = films[common.film_types[0]]
        film = films[button - 1]
        try:
            set_film_info(film)
            caption = ''
            if film.description:
                caption = film.description
            await bot.send_photo(message.from_user.id, film.image,
                                 caption=caption)
        except requests.exceptions.ConnectionError:
            await bot.send_message(message.from_user.id, film.url)
        # print(film.image)
        # print(film.description)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(FilmStates.FILM_STATE_0)


@dp.message_handler(state='*')
async def search_film(message: types.Message):
    print(message.text)
    state = dp.current_state(user=message.from_user.id)
    film_name = message.text
    films = find_top_five_by_name(film_name)
    if not films:
        message.reply("К сожалению, по твоему запросу ничего не найдено :(\n")
        return
    LAST_SEARCH_FOR_USER[message.from_user.id] = films
    msg = list_of_films(films)
    await state.set_state(FilmStates.all()[1])
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,  one_time_keyboard=True)
    num_of_films = sum([len(movies) for movies in films.values()])
    keyboard.add(*buttons[:num_of_films], button_no)
    await message.reply(msg, reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
