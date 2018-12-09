import datetime as dt
import logging
from logging.handlers import RotatingFileHandler
import os
import requests

import aiogram
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor, exceptions
from aiogram.utils.helper import Helper, HelperMode, ListItem

from search.parse_film_page import set_film_info
from search.parse_film_query import find_top_five_by_name, list_of_films
from search.search_in_yahoo import list_of_links
from search import utils


logger = logging.getLogger()
handler = RotatingFileHandler('log.txt', maxBytes=5 * 1024 * 1024,
                              backupCount=2)

formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

bot = aiogram.Bot(token=os.environ['BOT_TOKEN'])
dp = aiogram.dispatcher.Dispatcher(bot, storage=MemoryStorage())


class FilmStates(Helper):
    mode = HelperMode.snake_case
    FILM_STATE_0 = ListItem()
    FILM_STATE_1 = ListItem()


@dp.message_handler(state='*', commands=['start', 'help'])
async def send_welcome(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await message.reply(utils.MESSAGES['start'])
    await state.set_state(FilmStates.FILM_STATE_0)


@dp.message_handler(state=FilmStates.FILM_STATE_1)
async def choose_film(message: types.Message):
    if message.text not in utils.CHOICES.values():
        await bot.send_message(message.from_user.id,
                               utils.MESSAGES['another_film'])
    elif message.text == utils.CHOICES[7]:
        await bot.send_message(message.from_user.id,
                               utils.MESSAGES['nothing_matches'])
    else:
        button = int(message.text)
        films = utils.LAST_SEARCH_FOR_USER[message.from_user.id]
        if utils.FILM_TYPES[0] in films:
            if button > len(films[utils.FILM_TYPES[0]]):
                button -= len(films[utils.FILM_TYPES[0]])
                films = films[utils.FILM_TYPES[1]]
            else:
                films = films[utils.FILM_TYPES[0]]
        else:
            films = films[utils.FILM_TYPES[1]]
        film = films[button - 1]
        try:
            try:
                set_film_info(film)
                caption = ''
                if film.description:
                    caption_index = film.description[:utils.CAPTION_SIZE]
                    caption_index = caption_index.rfind('.') + 1
                    caption = film.description[:caption_index]
                logger.info(str(message.from_user.id) + ' ' + film.name +
                            ' ' + film.image + ' ' + str(film.description))
                if film.description:
                    if film.image.startswith(utils.NO_POSTER):
                        await bot.send_message(message.from_user.id,
                                               film.description)
                    else:
                        await bot.send_photo(message.from_user.id, film.image,
                                             caption=caption)
                else:
                    raise utils.NoPhotoAndDescription
            except (requests.exceptions.ConnectionError,
                    exceptions.WrongFileIdentifier,
                    utils.NoPhotoAndDescription) as exc:
                logger.exception(exc)
                await bot.send_message(message.from_user.id, film.url)
            if (dt.datetime.utcnow().year <
                    dt.datetime.strptime(film.year[2:6], '%Y').year):
                await bot.send_message(message.from_user.id,
                                       utils.MESSAGES['not_released'])
            else:
                await bot.send_message(message.from_user.id,
                                       utils.MESSAGES['list_of_links'] +
                                       list_of_links(film), parse_mode='HTML')
        except Exception as exc:
            logger.exception(exc)
            await bot.send_message(message.from_user.id,
                                   utils.MESSAGES['smth_went_wrong'])
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(FilmStates.FILM_STATE_0)


@dp.message_handler(state='*')
async def search_film(message: types.Message):
    logger.info(str(message.from_user.id) + ' ' + message.text)
    state = dp.current_state(user=message.from_user.id)
    film_name = message.text
    try:
        films = find_top_five_by_name(film_name)
    except utils.BadStatusCode as exc:
        logger.exception(exc)
        await bot.send_message(message.from_user.id,
                               utils.MESSAGES['exception'])
        return
    if not films:
        await message.reply(utils.MESSAGES['not_found'])
        return
    utils.LAST_SEARCH_FOR_USER[message.from_user.id] = films
    msg = list_of_films(films)
    await state.set_state(FilmStates.all()[1])
    keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                 one_time_keyboard=True)
    num_of_films = sum([len(movies) for movies in films.values()])
    keyboard.add(*utils.BUTTONS[:num_of_films], utils.BUTTON_NO)
    await message.reply(msg, reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
