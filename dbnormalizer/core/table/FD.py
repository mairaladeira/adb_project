__author__ = 'Maira'


class FD:
    def __init__(self):
        self.lhs = {}
        self.rhs = {}

    def set_lhs(self, lhs):
        self.lhs = lhs

    def set_rhs(self, rhs):
        self.rhs = rhs

    @property
    def get_lhs(self):
        return self.lhs

    @property
    def get_rhs(self):
        return  self.rhs