import urllib
import requests
import re
import html

kinopoisk_url = 'https://www.kinopoisk.ru/'


class Film:
    def __init__(self, name, url, year):
        self.name = name
        self.url = url
        self.year = year


def parse_a_tag(tag):
    name = re.search(b'data-type[\W\w]*?</a>', tag).group(0)[:-4]
    name = re.split(b'>', name)[1].decode(encoding='cp1251')
    name = html.unescape(name)
    url = re.search(b'film/[0-9]*', tag).group(0).decode(encoding='cp1251')
    year = re.search(b'"year">[\W\w]*?<', tag)
    if year:
        year = year.group(0)[7:-1].decode(encoding='cp1251')
        year = html.unescape(year)
    return Film(name, url, year)


def find_top_five_by_name(film):
    film = urllib.parse.quote(film)
    search_response = requests.get(kinopoisk_url + 'index.php?kp_query='
                                   + film + '&what=')
    if search_response.status_code != 200:
        print('Something went wrong...')
        return
    found_tags = [match for match in re.findall(
        b'<p class="name"><a href="/level/1/film/[0-9]*/sr/1/[\W\w]*?</p>',
        search_response.content)][:5]
    found_films = [parse_a_tag(tag) for tag in found_tags]
    return found_films


def list_of_films(films):
    res = ''
    if films:
        for i in range(len(films)):
            res += '{}. {}, {}\n'.format(i + 1, films[i].name, films[i].year or '-')
    else:
        res = "К сожалению, по твоему запросу ничего не найдено :(\n"
    return res[:-1]