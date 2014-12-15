from dbnormalizer.core.normalizer.NF import NF
from dbnormalizer.core.normalizer.NF3 import NF3

__author__ = 'Maira'


class BCNF(NF):
    def __init__(self):
        super()
        self.nf3 = NF3
        self.candidate_keys = {'pizza'}

    def is_bcnf(self, fds):
        for fd in fds:
            lhs = fds.get_lhs()
            rhs = fds.get_rhs()
            is_nf3 = NF3.is_nf3(lhs, rhs)
            if not is_nf3:
                return False
            for f in lhs:
                if f not in self.candidate_keys:
                    return False
        return True