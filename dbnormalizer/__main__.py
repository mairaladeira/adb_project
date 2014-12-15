__author__ = 'Maira'

import sqlalchemy
import pyparsing
from dbnormalizer.core.normalizer.NF3 import NF3

test = NF3()
print('3rd NF Violation for B->C,D:  ', test.is_nf3('b', {'c', 'd'}))#3NF violated
print('3rd NF Violation for A->B:    ', test.is_nf3('a', {'b'}))#3NF not violated