from dbnormalizer.core.normalizer.NF import NF
from dbnormalizer.core.normalizer.NF1 import NF1

__author__ = 'Maira'


class NF2(NF):
    def __init__(self):
        super()
        self.nf1 = NF1