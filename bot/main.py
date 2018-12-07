from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from kinopoisk.parse_query import find_top_five_by_name, list_of_films

from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='663290175:AAGT2h1895I-xZ_7Ma2VsqcyrQDa2ecV7p8')
dp = Dispatcher(bot, storage=MemoryStorage())


CHOICES = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: 'Ничего не подходит'}


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
        await message.reply("Поищем другой фильм? Пиши название!")
    elif message.text == CHOICES[6]:
        await message.reply("Попробуй уточнить название для более качественного поиска.")
    else:
        film = LAST_SEARCH_FOR_USER[message.from_user.id][int(message.text) - 1]
        await message.reply("Ты выбрал {}, {}".format(film.name, film.year))
        await message.reply(film.url)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(FilmStates.FILM_STATE_0)


@dp.message_handler(state='*')
async def search_film(message: types.Message):
    print(message.text)
    state = dp.current_state(user=message.from_user.id)
    film_name = message.text
    films = find_top_five_by_name(film_name)
    LAST_SEARCH_FOR_USER[message.from_user.id] = films
    msg = list_of_films(films)
    await state.set_state(FilmStates.all()[1])
    await message.reply(msg)


@dp.message_handler(commands=['search_film'])
async def send_question(message: types.Message):
    await message.reply("Какой фильм будем искать?")


if __name__ == '__main__':
    executor.start_polling(dp)
