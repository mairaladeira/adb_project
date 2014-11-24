from src.core.normalizer.NF import NF
from src.core.normalizer.NF2 import NF2

__author__ = 'Maira'


class NF3(NF):
    def __init__(self):
        super()
        self.nf2 = NF2