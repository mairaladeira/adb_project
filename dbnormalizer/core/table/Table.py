__author__ = 'Maira'
from itertools import combinations


class Table:
    def __init__(self, name):
        self.name = name
        #Table attributes will be a list of attribute objects
        self.attributes = []
        #Table fds will be a list of fd objects
        self.fds = []
        #pk is just a list of strings, eases comparing if an attribute is pk
        self.pk = []
        #for tables imported from the db
        self.imported_fk = []
        self.exported_fk = []
        #to add when generating a normalization proposal
        self.f_keys = []
        self.db_row_count = 0
        self.nf = 'not defined'

    def set_attributes(self, attributes):
        self.attributes = attributes

    def set_fds(self, fds):
        self.fds = fds

    def add_fd(self, fd):
        self.fds.append(fd)

    def add_attr(self, attr):
        self.attributes.add(attr)


    # tbd - implement a function which removes the fd
    # def remove_fd(self, fd):
    #     self.fds.remove(fd)

    @property
    def get_name(self):
        return self.name

    @property
    def get_attributes(self):
        return self.attributes

    @property
    def get_fds(self):
        return self.fds

    def get_fd_by_id(self, fd_id):
        k = 0
        for fd in self.fds:
            if fd_id == k:
                return fd
            k += 1
        return None

    def get_attribute_by_name(self, name):
        for attr in self.attributes:
            if attr.get_name == name:
                return attr

    def get_foreign_keys(self):
        return self.f_keys

    def get_attribute_string_list(self):
        list = []
        for att in self.attributes:
            list.append(att.name)
        return list

    def get_attribute_string_list_no_pk(self):
        list = []
        for att in self.attributes:
            if att.name not in self.pk:
                list.append(att.name)
        return list

    def get_attribute_string_list_combined(self):
        list = []
        L = self.get_attribute_string_list_no_pk()
        for x in range(1, len(L)):
            l = [",".join(map(str, comb)) for comb in combinations(L, x)]
            for el in l:
                list.append(el)
        return list

    def get_attribute_list_no_primary(self):
        list = []
        L = []
        for att in self.attributes:
            if att.name not in self.pk:
                L.append(att.name)
        #L = self.get_attribute_string_list()
        for x in range(1, len(L)):
            l = [",".join(map(str, comb)) for comb in combinations(L, x)]
            for el in l:
                list.append(el)
        return list

    def delete_fds(self, lhs_list_n, rhs_list_n):
        for f in self.fds:
            if set([a.get_name for a in f.get_lhs]) == set(lhs_list_n) and set([a.get_name for a in f.get_rhs]) == set(rhs_list_n):
                self.fds.remove(f)