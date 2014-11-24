__author__ = 'Maira'


class FKey:
    def __init__(self):
        self.table = {}
        self.attribute = {}
        self.fTable = {}

    def set_table(self, table):
        self.table = table

    def set_attribute(self, attribute):
        self.attribute = attribute

    def set_ftable(self, table):
        self.fTable = table

    @property
    def get_table(self):
        return self.table

    @property
    def get_attribute(self):
        return self.attribute

    @property
    def get_ftable(self):
        return self.fTable