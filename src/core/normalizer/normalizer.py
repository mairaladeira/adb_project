__author__ = 'Maira'


class Normalizer:
    def __init__(self):
        self.table = {}
        self.normalizer = {}

    def set_table(self, table):
        self.table = table

    def set_normalizer(self, normalizer):
        self.normalizer = normalizer

    @property
    def get_table(self):
        return self.table

    @property
    def get_normalizer(self):
        return self.normalizer