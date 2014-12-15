__author__ = 'Maira'

import sqlalchemy
import pyparsing

from dbnormalizer.core.table.FD import FD
from dbnormalizer.core.normalizer.BCNF import BCNF

#fd1 = FD(['pizza'], ['topping'])
#fd2 = FD(['topping'], ['topping_type'])

#fds = [fd1, fd2]
#print(fd1.get_lhs)


fd3 = FD('pizza', {'topping'})       #not voilated here
fd4 = FD('topping', {'topping_type'})  # voilated here
bcnf = BCNF()

fds = [fd4, fd3]
print('Is it in BCNF NF? :  ', bcnf.is_bcnf(fds))   #3NF violated
