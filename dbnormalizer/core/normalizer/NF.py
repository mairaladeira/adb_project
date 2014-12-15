__author__ = 'Maira'


class NF:
    def __init__(self):
        self.table = {}
        self.candidate_keys = {}

    #get all the candidates keys for the normal forms
    def get_candidate_keys(self):
        return self.candidate_keys

    def is_key_attribute(self, attribute):
        is_key_attr = False
        for e in self.candidate_keys:
                if e == attribute:
                    is_key_attr = True
        return is_key_attr