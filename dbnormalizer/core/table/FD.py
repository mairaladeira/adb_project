__author__ = 'Maira'


class FD:
    def __init__(self, lhs, rhs, imported=False):
        self.lhs = lhs
        self.rhs = rhs
        self.imported = imported

    @property
    def get_lhs(self):
        return self.lhs

    @property
    def get_rhs(self):
        return self.rhs

    def set_lhs(self, lhs):
        self.lhs = lhs

    def set_rhs(self, rhs):
        self.rhs = rhs