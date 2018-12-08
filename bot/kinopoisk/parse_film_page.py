import requests
import re
import html
from lxml.html import fromstring
from itertools import cycle

from . import common


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


proxies = get_proxies()
proxy_pool = cycle(proxies)


def get_img_url(pattern):
    return common.kinopoisk_url + pattern.split('\'')[1][1:]


def get_description(pattern):
    start = re.search('>', pattern).start() + 1
    return pattern[start:-6].replace('<br>', '\n')


def set_film_info(film):
    proxy = next(proxy_pool)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
    try:
        search_response = requests.get(film.url, headers=headers, timeout=5, proxies={"http": proxy, "https": proxy})
    except ConnectionError:
        print("Skipping. Connnection error")
        return set_film_info(film)
    print(film.url)
    if search_response.status_code != 200:
        print('Something went wrong...')
        return
#    print((search_response.content.decode(encoding='cp1251')))
    img_pattern = re.search('openImgPopup\(\'[\W\w]*?\'\)', search_response.text)
    print(img_pattern)
    img_url = None
    if img_pattern:
        img_url = get_img_url(img_pattern.group(0))
        print(img_url)
        if img_url == common.no_poster_url:
            img_url = None
    film.set_image(img_url)

    description = re.search('<div class="brand_words '
                            'film-synopsys"[\W\w]*?<\/div>',
                            search_response.text)
    if description:
        description = description.group(0)
        description = get_description(html.unescape(description))
        print(description)
    film.set_description(description)
    return film
