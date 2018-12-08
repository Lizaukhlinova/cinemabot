import urllib
import requests
from bs4 import BeautifulSoup

from . import film
from . import common


def parse_a_tag(tag):
    a_tag = tag.find('a', {'class': 'link link-holder'})
    name = a_tag.text
    url = a_tag['href']
    year = tag.findAll('span', {'class': 'text'})[-1].text
    return film.Film(name, url, year)


def find_top_five_by_name(film_name):
    film_name = urllib.parse.quote(film_name)
    search_response = requests.get(film.mail_url + '/search/?region_id=70&q='
                                   + film_name, headers=common.HEADERS)
    if search_response.status_code != 200:
        print('Something went wrong...')
        return
    soup = BeautifulSoup(search_response.content, features="lxml")
    found_tags = soup.findAll("div", {"class": "searchitem__item"})[:5]
    found_films = [parse_a_tag(tag) for tag in found_tags]
    return found_films


def list_of_films(films):
    res = ''
    for i in range(len(films)):
        res += '{}. {}, {}\n'.format(i + 1, films[i].name, films[i].year or '-')
    return res[:-1]
