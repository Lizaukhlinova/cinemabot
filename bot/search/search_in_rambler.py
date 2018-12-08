from aiogram.utils import markdown

import urllib
import requests
from bs4 import BeautifulSoup

from . import common


def find_top_five_links(film):
    query = film.name + ' ' + film.year + common.watch_online
    query = urllib.parse.quote(query)
    search_response = requests.get(common.rambler_url + query)
    soup = BeautifulSoup(search_response.content)
    serp_list = soup.find('div', {'class': 'b-serp-list'})
    serp_items = serp_list.findAll('span', {'class': 'b-serp-item__info'})
    links = [tag.find('a')['href'] for tag in serp_items]
    return links


def list_of_links(film):
    links = find_top_five_links(film)
    res = ''
    for i in range(len(links)):
        title = urllib.parse.urlparse(links[i]).netloc
        res += '{}. {}\n'.format(i, markdown.hlink(title, links[i]))
