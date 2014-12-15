from dbnormalizer.core.normalizer.NF import NF
from dbnormalizer.core.normalizer.NF2 import NF2

__author__ = 'Maira'


def is_key_attribute(attribute):
    is_key_attr = False
    candidate_keys = {'a'}

    for e in candidate_keys:
            if e == attribute:
                is_key_attr = True
    return is_key_attr


class NF3(NF):
    def __init__(self):
        super()
        self.nf2 = NF2
        self.is_nf2 = True

    #for 1st functional dependency it will give TRUE as it is in 3NF A->B   A is a PK
    #for 2nd functional dependency it will give FALSE as it is not in 3NF B->C and B is not PK
    #(these both are for same table)
            #fdsLHS ='a'
            #fdsRHS ='b'
            #fdsLHS ='b'
            #fdsRHS ={'c','d'}
    def is_nf3(self, fds_lhs, fds_rhs):
        candidate_keys = {'a', 'e', 'f'}
        third_nf_violates = False
        #fdsLHS=functional_dependencies.getLHS_dep();
        #fdsRHS=functional_dependencies.getRHS_dep();
        if not self.is_nf2:
            return False
        lhs_is_super_key = False

        try:
            for e in candidate_keys:
                    if e == fds_lhs:
                        lhs_is_super_key = True

            if not lhs_is_super_key:
                for r in fds_rhs:
                    if not is_key_attribute(r):
                        third_nf_violates = True

        except Exception as ex:
            print('violates_3NF excepion')
            print(ex)

        return third_nf_violates

