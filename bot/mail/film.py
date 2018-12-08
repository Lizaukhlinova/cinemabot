mail_url = 'https://kino.mail.ru'


class Film:
    def __init__(self, name, url, year):
        self.name = name
        self.url = mail_url + url
        self.year = year
        self.image = None
        self.description = None

    def set_image(self, image):
        if image.startswith('/'):
            image = mail_url + image
        self.image = image

    def set_description(self, description):
        self.description = description

    def print(self):
        print(self.name, self.year, self.image, self.description)
