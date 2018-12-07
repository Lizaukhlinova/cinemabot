import common


class Film:
    def __init__(self, name, url, year):
        self.name = name
        self.url = common.kinopoisk_url + url
        self.year = year
        self.image = None
        self.description = None

    def set_image(self, image):
        self.image = image

    def set_description(self, description):
        self.description = description
