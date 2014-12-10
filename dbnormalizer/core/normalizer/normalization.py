__author__ = 'Maira'


class Normalization:
    def __init__(self):
        self.tables = {}
        self.fds = {}
        self.fkeys = {}

    def set_tables(self, tables):
        self.tables = tables

    def set_fds(self, fds):
        self.fds = fds

    def set_fkeys(self, fkeys):
        self.fkeys = fkeys

    @property
    def get_tables(self):
        return self.tables

    @property
    def get_fds(self):
        return self.fds

    @property
    def get_fkeys(self):
        return self.fkeys