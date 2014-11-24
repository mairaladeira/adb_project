from src.core.normalizer.NF import NF
from src.core.normalizer.NF3 import NF3

__author__ = 'Maira'


class BCNF(NF):
    def __init__(self):
        super()
        self.nf3 = NF3