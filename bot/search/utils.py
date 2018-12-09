from aiogram.types import KeyboardButton


class NoPhotoAndDescription(Exception):
    pass


class BadStatusCode(Exception):
    pass


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; '
                  'rv:45.0) Gecko/20100101 Firefox/45.0'
}

film_types = ['Фильмы', 'Сериалы']

mail_url = 'https://kino.mail.ru'

rambler_url = ('https://nova.rambler.ru/search?&utm_source=r0'
               '&utm_campaign=self_promo&utm_medium=form&utm_content=search&query=')

watch_online = ' смотреть онлайн'

yahoo_url = ('https://ru.search.yahoo.com/search;_ylt=AwrJQ56mLQ1cPxsAzw3Kxgt.;'
             '_ylc=X1MDMjExNDcwMTAwMgRfcgMyBGZyAwRncHJpZANnTzlkb3NEWVNqdWREVHNOd'
             'Upjd1BBBG5fcnNsdAMwBG5fc3VnZwM2BG9yaWdpbgNydS5zZWFyY2gueWFob28uY29t'
             'BHBvcwMwBHBxc3RyAwRwcXN0cmwDBHFzdHJsAzE5OARxdWVyeQMlRDAlQkMlRDAlQjA'
             'lRDAlQkIlRDElOEMlRDElODclRDAlQjglRDElODglRDAlQkQlRDAlQjglRDAlQkElMj'
             'AlRDAlQjIlMjAlRDAlQjIlRDAlQjUlRDAlQjMlRDAlQjAlRDElODElRDAlQjUlMjAlR'
             'DElODElRDAlQkMlRDAlQkUlRDElODIlRDElODAlRDAlQjUlRDElODIlRDElOEMlMjAl'
             'RDAlQkUlRDAlQkQlRDAlQkIlRDAlQjAlRDAlQjklRDAlQkQEdF9zdG1wAzE1NDQzNjc'
             '1MzQ-?fr2=sb-top-ru.search&fr=sfp&iscqry=&p=')

caption_max_size = 1024

no_poster = 'https://kino.mail.ru/img/v2/nopicture/'

CHOICES = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: 'Ничего не подходит'}


buttons = [KeyboardButton(CHOICES[1]),
           KeyboardButton(CHOICES[2]),
           KeyboardButton(CHOICES[3]),
           KeyboardButton(CHOICES[4]),
           KeyboardButton(CHOICES[5]),
           KeyboardButton(CHOICES[6])]
button_no = KeyboardButton(CHOICES[7])


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

}

LAST_SEARCH_FOR_USER = {}
