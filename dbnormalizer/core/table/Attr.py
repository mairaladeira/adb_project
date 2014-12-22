__author__ = 'Maira'


class Attribute:
    def __init__(self, name):
        self.name = name
        self.type = ''

    def set_type(self, t):
        self.type = t

    @property
    def get_name(self):
        return self.name

    @property
    def get_type(self):
        return self.type