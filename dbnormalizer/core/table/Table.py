__author__ = 'Maira'


class Table:
    def __init__(self, name):
        self.name = name
        #Table attributes will be a list of attribute objects
        self.attributes = []
        #Table fds will be a list of fd objects
        self.fds = []

    def set_attributes(self, attributes):
        self.attributes = attributes

    def set_fds(self, fds):
        self.fds = fds

    @property
    def get_name(self):
        return self.name

    @property
    def get_attributes(self):
        return self.attributes

    @property
    def get_fds(self):
        return self.fds