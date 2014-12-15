__author__ = 'Maira'

import sqlalchemy
import pyparsing

#from dbnormalizer.core.importdata.XMLImport import XMLImport


#test = XMLImport('/Users/mairamachadoladeira/PycharmProjects/adb_project/examples/test.xml')
#test.readfile()


from dbnormalizer.core.table.FD import FD
from dbnormalizer.core.normalizer.NF3 import NF3

#fd1 = FD(['pizza'], ['topping'])
#fd2 = FD(['topping'], ['topping_type'])

#fds = [fd1, fd2]
#print(fd1.get_lhs)

fd3 = FD(['b'], ['c','d'])
fd4 = FD(['a'], ['b'])
fds = [fd3, fd4]
print(fd3.get_lhs)

print(NF3.is_nf3(fds))   #3NF violated
#print('3rd NF Violation for A->B:    ', NF3.is_nf3('a', {'b'}));   #3NF not violated
