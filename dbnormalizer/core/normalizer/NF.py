__author__ = 'Maira'

from dbnormalizer.core.table.FD import FD
from dbnormalizer.core.table.Table import Table

class NF:
    def __init__(self):
        self.table = {}
        self.candidate_keys = {}

    #get all the candidates keys for the normal forms
    def get_candidate_keys(self, table):
        candidate_keys=[]
        candidate_singleton=[]
        allattrs = table.get_attributes
        allattrnames = [n.name for n in allattrs]
        workattrs = table.get_attributes
        for a in allattrs:
            cover = self.get_attr_closure([a],table)
            covernames = [n.name for n in cover]
            if set(allattrnames) <= set(covernames):
                candidate_keys.append([a])
                candidate_singleton.append(a)
        workattrs = list(set(workattrs)-set(candidate_singleton))
        x = len(workattrs)
        powerset=[]
        for i in range(1,1 << x):
            powerset.append([workattrs[j] for j in range(x) if (i & (1 << j))])
        for p in powerset:
            stop=0
            if len(candidate_keys)>=1:
                for c in candidate_keys:
                    if set(c) <= set(p):
                        stop = 1
            if stop<1:
                cover = self.get_attr_closure(p,table)
                covernames = [n.name for n in cover]
                if set(allattrnames) <= set(covernames):
                    candidate_keys.append(p)
        return candidate_keys


    def is_prime_attribute(self, table, attribute):
        is_prime_attr = False
        for e in self.get_candidate_keys(table):
            enames = [n.name for n in e]
            if set([attribute.name]) <= set(enames):
                is_prime_attr = True
        return is_prime_attr

    def is_key_attribute(self, attribute):
        is_key_attr = False
        for e in self.candidate_keys:
                if e == attribute:
                    is_key_attr = True
        return is_key_attr

    def set_table(self, table):
        self.table = table

    def get_attr_closure(self,attr_list,table):
        attr1 = table.get_attributes
        fd1 = table.get_fds
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
                        if not(set([right_e.name]) <= set(left_names)):
                            left_closure.append(right_e)
            if left_closure_len_init == len(left_closure):
                stopper = 1
        return left_closure

    def get_mincover(self, table):
        attrs = [attrib.name for attrib in table.get_attributes]
        # first step: split rhs
        fd_1 = []
        for fd in table.get_fds:
            for right_e in fd.rhs:
                fd_1.append(FD(fd.get_lhs,[right_e]))
        step1_table = Table(table.get_name)
        step1_table.set_attributes(table.get_attributes)
        step1_table.set_fds(fd_1)
        # second step: check for attribute redundancy in lhs
        fd_2 = []
        step2_table = Table(table.get_name)
        step2_table.set_attributes(table.get_attributes)
        for fd1 in step1_table.get_fds:
            if len(fd1.get_lhs) == 1:
                fd_2.append(FD(fd1.get_lhs,fd1.get_rhs))
            else:
                a=fd1.get_lhs
                for left in a:
                    left_closure = []
                    left_closure.append(left)
                    stopper = 0
                    while stopper == 0:
                        left_closure_len_init = len(left_closure)
                        for fd in step1_table.get_fds:
                            fdlhs = [l.name for l in fd.get_lhs]
                            left_names = [n.name for n in left_closure]
                            if set(fdlhs) <= set(left_names):
                                for right_e in fd.get_rhs:
                                    if not(set([right_e.name]) < set(left_names)):
                                        left_closure.append(right_e)
                        if left_closure_len_init == len(left_closure):
                            stopper = 1
                    left_closure_names = [n.name for n in left_closure]
                    for left_2 in a:
                        if left.name != left_2.name:
                            if set([left_2.name]) <= set(left_closure_names):
                                a.remove(left_2)
                fd_2.append(FD(a,fd1.get_rhs))
        step2_table.set_fds(fd_2)
        # third step: remove redundant FDs
        fd_3 = []
        step3_table = Table(table.get_name)
        step3_table.set_attributes(table.get_attributes)
        for fd1 in step2_table.get_fds:
            temp = []
            for x in step2_table.get_fds:
                temp.append(x)
            temp.remove(fd1)
            a=fd1.get_lhs
            b=fd1.get_rhs
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
                            if not(set([right_e.name]) <= set(left_names)):
                                left_closure.append(right_e)
                if left_closure_len_init == len(left_closure):
                    stopper = 1
            left_closure_names = [n.name for n in left_closure]
            c = []
            for right_2 in b:
                if not(set([right_2.name]) <= set(left_closure_names)):
                    c.append(right_2)
            if len(c)>0:
                 fd_3.append(FD(a,c))
        step3_table.set_fds(fd_3)
        return fd_3



