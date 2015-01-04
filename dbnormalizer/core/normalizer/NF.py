__author__ = 'Maira'

from dbnormalizer.core.table.FD import FD
from dbnormalizer.core.table.Table import Table

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

    def set_table(self, table):
        self.table = table

    # @property
    def get_mincover(self, table):
        attrs = [attrib.name for attrib in table.get_attributes]
        for fd in table.get_fds:
            fdlhs = [l.name for l in fd.get_lhs]
            fdrhs = [r.name for r in fd.get_rhs]
        # first step: split rhs
        fd_1 = []
        for fd in table.get_fds:
            for right_e in fd.rhs:
                fd_1.append(FD(fd.get_lhs,[right_e]))
        step1_table = Table(table.get_name)
        step1_table.set_attributes(table.get_attributes)
        step1_table.set_fds(fd_1)
        for fd in step1_table.get_fds:
            fdlhs = [l.name for l in fd.get_lhs]
            fdrhs = [r.name for r in fd.get_rhs]
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
                    left_closure_len_curr = 0
                    while stopper == 0:
                        left_closure_len_init = len(left_closure)
                        for fd in step1_table.get_fds:
                            fdlhs = [l.name for l in fd.get_lhs]
                            fdrhs = [r.name for r in fd.get_rhs]
                            left_names = [n.name for n in left_closure]
                            if set(fdlhs) <= set(left_names):
                                for right_e in fd.get_rhs:
                                    if not(set([right_e.name]) < set(left_names)):
                                        left_closure.append(right_e)
                            left_names = [n.name for n in left_closure]
                        if left_closure_len_init == len(left_closure):
                            stopper = 1
                    left_closure_names = [n.name for n in left_closure]
                    for left_2 in a:
                        if left.name != left_2.name:
                            if set([left_2.name]) <= set(left_closure_names):
                                a.remove(left_2)
                fd_2.append(FD(a,fd1.get_rhs))
        step2_table.set_fds(fd_2)
        for fd in step2_table.get_fds:
            fdlhs = [l.name for l in fd.get_lhs]
            fdrhs = [r.name for r in fd.get_rhs]
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
            for left in a:
                left_closure = []
                left_closure.append(left)
            stopper = 0
            left_closure_len_curr = 0
            while stopper == 0:
                left_closure_len_init = len(left_closure)
                for fd in temp:
                    fdlhs = [l.name for l in fd.get_lhs]
                    fdrhs = [r.name for r in fd.get_rhs]
                    left_names = [n.name for n in left_closure]
                    if set(fdlhs) <= set(left_names):
                        for right_e in fd.get_rhs:
                            if not(set([right_e.name]) <= set(left_names)):
                                left_closure.append(right_e)
                    left_names = [n.name for n in left_closure]
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
        for fd in step3_table.get_fds:
            fdlhs = [l.name for l in fd.get_lhs]
            fdrhs = [r.name for r in fd.get_rhs]
        # step 4: combine rhs
        # fd_4 = []
        # processed_left = []
        # step4_table = Table(table.get_name)
        # step4_table.set_attributes(table.get_attributes)
        # for fd in step3_table.get_fds:
        #     for left in fd.get_lhs:
        #         r = []
        #         for fd2 in step3_table.get_fds:
        #             for left2 in fd2.get_lhs:
        #                 if left.name == left2.name:
        #                     for right2 in fd2.get_rhs:
        #                         r.append(right2)
        #     if not(set(left.name) <= set(processed_left)):
        #         fd_4.append(FD(fd.get_lhs,r))
        #         processed_left.append(left.name)
        # step4_table.set_fds(fd_4)
        # print("Step 4: FD List")
        # for fd in step4_table.get_fds:
        #     fdlhs = [l.name for l in fd.get_lhs]
        #     fdrhs = [r.name for r in fd.get_rhs]
        #     # print(fd.get_rhs.name)
        #     print(fdlhs,"->",fdrhs)
        return fd_3