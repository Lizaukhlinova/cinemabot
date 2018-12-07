import requests
import re
import html

from . import common


def get_img_url(pattern):
    return common.kinopoisk_url + pattern.split('\'')[1][1:]


def get_description(pattern):
    start = re.search('>', pattern).start() + 1
    return pattern[start:-6].replace('<br>', '\n')


def parse_page(film):
    search_response = requests.get(film.url)
    if search_response.status_code != 200:
        print('Something went wrong...')
        return
    img_pattern = re.search(b'openImgPopup\(\'[\W\w]*?\'\)',
                            search_response.content).group(0)
    img_url = get_img_url(img_pattern.decode('cp1251'))
    if img_url == common.no_poster_url:
        img_url = None
    film.set_image(img_url)

    description = re.search(b'<div class="brand_words '
                            b'film-synopsys"[\W\w]*?<\/div>',
                            search_response.content)
    if description:
        description = description.group(0).decode('cp1251')
        description = get_description(html.unescape(description))
    film.set_description(description)
