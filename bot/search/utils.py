from aiogram.types import KeyboardButton


class NoPhotoAndDescription(Exception):
    pass


class BadStatusCode(Exception):
    pass


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; '
                  'rv:45.0) Gecko/20100101 Firefox/45.0'
}

FILM_TYPES = ['Фильмы', 'Сериалы']

TOP_SIZE_BY_TYPE = {
    'Фильмы': 5,
    'Сериалы': 3,
}

MAIL_URL = 'https://kino.mail.ru'

YAHOO_URL = ('https://ru.search.yahoo.com/search;_ylt=AwrJQ56mLQ1cPxsAzw3Kxgt.;'
             '_ylc=X1MDMjExNDcwMTAwMgRfcgMyBGZyAwRncHJpZANnTzlkb3NEWVNqdWREVHNOd'
             'Upjd1BBBG5fcnNsdAMwBG5fc3VnZwM2BG9yaWdpbgNydS5zZWFyY2gueWFob28uY29t'
             'BHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzE5OARxdWVyeQMlRDAlQkMlRDAlQjA'
             'lRDAlQkIlRDElOEMlRDElODclRDAlQjglRDElODglRDAlQkQlRDAlQjglRDAlQkElMj'
             'AlRDAlQjIlMjAlRDAlQjIlRDAlQjUlRDAlQjMlRDAlQjAlRDElODElRDAlQjUlMjAlR'
             'DElODElRDAlQkMlRDAlQkUlRDElODIlRDElODAlRDAlQjUlRDElODIlRDElOEMlMjAl'
             'RDAlQkUlRDAlQkQlRDAlQkIlRDAlQjAlRDAlQjklRDAlQkQEdF9zdG1wAzE1NDQzNjc'
             '1MzQ-?fr2=sb-top-ru.search&fr=sfp&iscqry=&p=')

CAPTION_SIZE = 1024

WATCH_ONLINE = ' смотреть онлайн'

NO_POSTER = 'https://kino.mail.ru/img/v2/nopicture/'

CHOICES = {
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: 'Ничего не подходит'}

BUTTONS = [KeyboardButton(CHOICES[1]),
           KeyboardButton(CHOICES[2]),
           KeyboardButton(CHOICES[3]),
           KeyboardButton(CHOICES[4]),
           KeyboardButton(CHOICES[5]),
           KeyboardButton(CHOICES[6]),
           KeyboardButton(CHOICES[7]),
           KeyboardButton(CHOICES[8])]
BUTTON_NO = KeyboardButton(CHOICES[9])


MESSAGES = {
    'start': 'Привет! Я подскажу тебе, где можно посмотреть твой любимый фильм онлайн. '
             'Просто набери название фильма или сериала и кликай на предлагаемые ссылки :)',
    'list_of_links': 'Попробуй посмотреть фильм здесь:\n\n',
    'not_released': 'Фильм еще не вышел в прокат, скорее всего, '
                    'его еще нельзя посмотреть онлайн.',
    'another_film': 'Поищем другой фильм? Пиши название!',
    'nothing_matches': 'Попробуй уточнить название для более '
                       'качественного поиска.',
    'exception': 'Извини, что-то пошло не так. :(',
    'not_found': 'К сожалению, по твоему запросу ничего не найдено :(',
    'smth_went_wrong': 'Извини, что-то пошло не так :('
}

LAST_SEARCH_FOR_USER = {}
