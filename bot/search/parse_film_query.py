import urllib
import requests
from bs4 import BeautifulSoup

from . import film
from . import utils


def _parse_a_tag(tag):
    a_tag = tag.find('a', {'class': 'link link-holder'})
    name = a_tag.text
    url = utils.mail_url + a_tag['href']
    year = tag.findAll('span', {'class': 'text'})[-1].text
    return film.Film(name, url, year)


def find_top_five_by_name(film_name):
    film_name = urllib.parse.quote(film_name)
    search_response = requests.get(utils.mail_url + '/search/?region_id=70&q='
                                   + film_name, headers=utils.HEADERS)
    if search_response.status_code != 200:
        raise utils.BadStatusCode('Bad code while searching films '
                                  + search_response.url)
    soup = BeautifulSoup(search_response.content, features='lxml')
    all_blocks = soup.findAll("div", {"class": "block"})
    blocks = {}
    for block in all_blocks:
        header = block.find('span', {'class': 'hdr__inner'})
        if header:
            if header.text in utils.film_types:
                blocks[header.text] = block
    found_items = {}
    for header, block in blocks.items():
        found_tags = block.findAll("div", {"class": "searchitem__item"})[:3]
        found_items[header] = [_parse_a_tag(tag) for tag in found_tags]
    return found_items


def list_of_films(films):
    res = ''
    i = 0
    for header in utils.film_types:
        if header in films:
            res += header + ':\n'
            for movie in films[header]:
                res += '{}. {}, {}\n'.format(i + 1, movie.name,
                                             movie.year or '-')
                i += 1
            res += '\n'
    return res[:-1]
