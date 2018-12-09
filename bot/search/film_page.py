import requests
from bs4 import BeautifulSoup

from . import common


def set_film_info(film):
    search_response = requests.get(film.url, timeout=5,
                                   headers=common.HEADERS)
    if search_response.status_code != 200:
        print('Something went wrong...')
        return
    soup = BeautifulSoup(search_response.content, features="lxml")
    div_tag = soup.find('div', {'class': 'block block_bg_gray padding_vertical_30 js-module'})
    photo = div_tag.find('span', {'class': 'photo__pic'})
    film.set_image(photo['style'][21:-1])
    description = div_tag.find('span', {'itemprop': 'description'})
    if description:
        description = description.text
    film.set_description(description)
