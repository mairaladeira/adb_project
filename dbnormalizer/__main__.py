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


fd3 = FD('a', {'b'})       #not voilated here
fd4 = FD('b', {'c', 'd'})  # voilated here
nf3 = NF3()

fds = [fd4,fd3]
print('Is it in 3rd NF? :  ',nf3.is_nf3(fds))   #3NF violated
