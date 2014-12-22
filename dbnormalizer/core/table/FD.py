__author__ = 'Maira'


class FD:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    @property
    def get_lhs(self):
        return self.lhs

    @property
    def get_rhs(self):
        return  self.rhs