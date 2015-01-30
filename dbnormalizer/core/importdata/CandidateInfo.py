__author__ = 'Iva'


class CandidateInfo:
    def __init__(self, attlist, sp):
        self.rhs_att = {}
        for att in attlist:
            self.rhs_att[att] = True
        self.stripped_partition = sp

    def set_RHS(self, attributes):
        for att in attributes:
            self.RHSatt[att] = True