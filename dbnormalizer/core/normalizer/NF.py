__author__ = 'Maira'

from dbnormalizer.core.table.FD import FD
from dbnormalizer.core.table.Table import Table


class NF:
    def __init__(self, table):
        self.table = table
        self.candidate_keys = self.calculate_candidate_keys()
        self.min_cover = self.calculate_mincover()
        self.violating_fds = []

    def get_min_cover(self):
        return self.min_cover

    def get_candidate_keys(self):
        return self.candidate_keys

    def get_violating_fds(self):
        return self.violating_fds

    def get_table(self):
        return self.table

    # determine the nf of the table. it returns the nf and the FDs breaking the next NF, and is used in the Table class
    def determine_nf(self):
        nf = '1NF'
        if self.is_nf2():
            nf = '2NF'
            if self.is_nf3():
                nf = '3NF'
                if self.is_bcnf():
                    nf = 'BCNF'
        self.table.nf = nf
        return nf



        # check isnf2,3,4 and return the nf of the table

    # def init_candidate_keys(self):
    # for t in self.tables:
    #         self.candidate_keys[t] = self.calculate_candidate_keys(t)

    #get all the candidates keys for the normal forms
    # returns the set of candidate keys - list of attributes or list of list of attributes (for composite keys)
    # for example [[a], [b,c]] , where a,b,c are of type Attribute
    def calculate_candidate_keys(self):
        candidate_keys = []
        candidate_singleton = []
        allattrs = self.table.get_attributes
        allattrnames = [n.name for n in allattrs]
        workattrs = self.table.get_attributes
        for a in allattrs:
            cover = self.get_attr_closure([a])
            covernames = [n.name for n in cover]
            if set(allattrnames) <= set(covernames):
                candidate_keys.append([a])
                candidate_singleton.append(a)
        workattrs = list(set(workattrs) - set(candidate_singleton))
        x = len(workattrs)
        powerset = []
        for i in range(1, 1 << x):
            powerset.append([workattrs[j] for j in range(x) if (i & (1 << j))])
        for p in powerset:
            stop = 0
            if len(candidate_keys) >= 1:
                for c in candidate_keys:
                    if set(c) <= set(p):
                        stop = 1
            if stop < 1:
                cover = self.get_attr_closure(p)
                covernames = [n.name for n in cover]
                if set(allattrnames) <= set(covernames):
                    candidate_keys.append(p)
        return candidate_keys


    def is_prime_attribute(self, attribute):
        is_prime_attr = False
        #        for e in self.calculate_candidate_keys(table):
        for e in self.candidate_keys:
            enames = [n.name for n in e]
            if {attribute.name} <= set(enames):
                is_prime_attr = True
        return is_prime_attr

    # we don't need a function is_key_attribute, since we have a is_prime_attribute - it's the same thing
    # def is_key_attribute(self, attribute):
    #     is_key_attr = False
    #     for e in self.candidate_keys:
    #             if e == attribute:
    #                 is_key_attr = True
    #     return is_key_attr

    # changed concept to work with one table at a time. not needed
    # def set_table(self, table):
    #     self.tables.append(table)

    def get_attr_closure(self, attr_list):
        attr1 = self.table.get_attributes
        fd1 = self.table.get_fds
        left_closure = []
        for left in attr_list:
            for attrib in attr1:
                if left.name == attrib.name:
                    left_closure.append(attrib)
        stopper = 0
        while stopper == 0:
            left_closure_len_init = len(left_closure)
            for fd in fd1:
                fdlhs = [l.name for l in fd.get_lhs]
                left_names = [n.name for n in left_closure]
                if set(fdlhs) <= set(left_names):
                    for right_e in fd.get_rhs:
                        if not ({right_e.name} <= set(left_names)):
                            left_closure.append(right_e)
            if left_closure_len_init == len(left_closure):
                stopper = 1
        return left_closure

    # returns a minimal cover - list of functional dependencies of a table. [fd1, fd2,...]
    # the fd's are of type FD
    def calculate_mincover(self):
        table = self.table
        # first step: split rhs
        fd_1 = []
        for fd in self.table.get_fds:
            for right_e in fd.rhs:
                fd_1.append(FD(fd.get_lhs, [right_e]))
        step1_table = Table(self.table.get_name)
        step1_table.set_attributes(self.table.get_attributes)
        step1_table.set_fds(fd_1)
        # second step: check for attribute redundancy in lhs
        fd_2 = []
        step2_table = Table(self.table.get_name)
        step2_table.set_attributes(self.table.get_attributes)
        for fd1 in step1_table.get_fds:
            if len(fd1.get_lhs) == 1:
                fd_2.append(FD(fd1.get_lhs, fd1.get_rhs))
            else:
                a = fd1.get_lhs
                for left in a:
                    left_closure = [left]
                    stopper = 0
                    while stopper == 0:
                        left_closure_len_init = len(left_closure)
                        for fd in step1_table.get_fds:
                            fdlhs = [l.name for l in fd.get_lhs]
                            left_names = [n.name for n in left_closure]
                            if set(fdlhs) <= set(left_names):
                                for right_e in fd.get_rhs:
                                    if not ({right_e.name} < set(left_names)):
                                        left_closure.append(right_e)
                        if left_closure_len_init == len(left_closure):
                            stopper = 1
                    left_closure_names = [n.name for n in left_closure]
                    for left_2 in a:
                        if left.name != left_2.name:
                            if {left_2.name} <= set(left_closure_names):
                                a.remove(left_2)
                fd_2.append(FD(a, fd1.get_rhs))
        step2_table.set_fds(fd_2)
        # third step: remove redundant FDs
        fd_3 = []
        step3_table = Table(self.table.get_name)
        step3_table.set_attributes(self.table.get_attributes)
        for fd1 in step2_table.get_fds:
            temp = []
            for x in step2_table.get_fds:
                temp.append(x)
            temp.remove(fd1)
            a = fd1.get_lhs
            b = fd1.get_rhs
            left_closure = []
            for left in a:
                left_closure.append(left)
            stopper = 0
            while stopper == 0:
                left_closure_len_init = len(left_closure)
                for fd in temp:
                    fdlhs = [l.name for l in fd.get_lhs]
                    left_names = [n.name for n in left_closure]
                    if set(fdlhs) <= set(left_names):
                        for right_e in fd.get_rhs:
                            if not ({right_e.name} <= set(left_names)):
                                left_closure.append(right_e)
                if left_closure_len_init == len(left_closure):
                    stopper = 1
            left_closure_names = [n.name for n in left_closure]
            c = []
            for right_2 in b:
                if not ({right_2.name} <= set(left_closure_names)):
                    c.append(right_2)
            if len(c) > 0:
                fd_3.append(FD(a, c))
        step3_table.set_fds(fd_3)
        return fd_3

    #determine if a table is in second NF, returns true/false
    def is_nf2(self):
        nf_good = True
        fds0 = self.table.get_fds
        fds = []
        for fd in fds0:
            for right_e in fd.rhs:
                fds.append(FD(fd.get_lhs, [right_e]))
        ck_names = []
        for n in self.candidate_keys:
            temp = [a.name for a in n]
            ck_names.append(temp)
        try:
            for fd in fds:
                lhs = fd.get_lhs
                rhs = fd.get_rhs
                for r in rhs:
                    if not self.is_prime_attribute(r):
                        if lhs not in self.candidate_keys:
                            lhsn = [l.name for l in lhs]
                            for c in ck_names:
                                if set(lhsn) < set(c):
                                    self.violating_fds.append(fd)
                                    nf_good = False
            return nf_good
        except Exception as ex:
            print('violates_2NF exception')
            print(ex)


    #differs from function in NF3 class in a way that it uses the table as an argument
    #tbd the fds and attributes in the algorithm need to be treated with respect to their class - Attribute and FD.
    def is_nf3(self):
        fds = self.table.get_fds
        nf_good = True
        lhs_is_super_key = False
        try:
            for fd in fds:
                lhs = fd.get_lhs
                rhs = fd.get_rhs
                ck_names=[]
                lhsn=[a.name for a in lhs]
                for e in self.candidate_keys:
                    temp=[a.name for a in e]
                    ck_names.append(temp)
                for e in ck_names:
                    lhs_is_super_key = False
                    if set(e) == set(lhsn):
                        lhs_is_super_key = True

                if not lhs_is_super_key:
                    for r in rhs:
                        if not self.is_prime_attribute(r):
                            self.violating_fds.append(fd)
                            nf_good = False
            return nf_good
        except Exception as ex:
            print('violates_3NF excepion')
            print(ex)




    #same thing as above, it uses a table as an argument
    def is_bcnf(self):
        fds = self.table.get_fds
        nf_good = True
        for fd in fds:
            lhs = fd.get_lhs
            lhsn=[a.name for a in lhs]
            ck_names=[]
            for e in self.candidate_keys:
                temp=[a.name for a in e]
                ck_names.append(temp)
            rhs = fd.get_rhs
            if not any(set(lhsn) == set(x) for x in ck_names):
                self.violating_fds.append(fd)
                nf_good = False

            # for f in lhs:
            #     if f not in self.candidate_keys:
            # for f in lhs:
            #     if f not in self.candidate_keys:
            #         return False
        return nf_good



# from dbnormalizer.core.importdata.XMLImport import XMLImport
# test = XMLImport(r'C:\Users\AlexGattino\PycharmProjects\adb_project\examples\test5.xml',True)
# test.init_objects()
# schema = test.get_schema()
#
# for table in schema.get_tables():
#     print(table.get_name)
#     nf = NF(table)
#     nf.determine_nf()
#     if table.nf != 'BCNF':
#         print(nf.violating_fds)
#     print(table.nf)
