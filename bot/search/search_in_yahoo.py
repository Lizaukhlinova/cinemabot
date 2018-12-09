from aiogram.utils import markdown

import urllib
import requests
from bs4 import BeautifulSoup

from . import utils


def _find_top_five_links(film):
    query = film.name + ' ' + film.year + utils.WATCH_ONLINE
    query = urllib.parse.quote(query)
    search_response = requests.get(utils.YAHOO_URL + query)
    soup = BeautifulSoup(search_response.content, features='lxml')
    serp_items = soup.findAll('div',
                              {'class': 'compTitle options-toggle'})[:5]
    links = [tag.find('a')['href'] for tag in serp_items]
    return links


def list_of_links(film):
    links = _find_top_five_links(film)
    res = ''
    for i in range(len(links)):
        title = urllib.parse.urlparse(links[i]).netloc
        res += '{}. {}\n'.format(i + 1, markdown.hlink(title, links[i]))
    return res
