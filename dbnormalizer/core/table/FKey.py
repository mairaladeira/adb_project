__author__ = 'Maira'


class FKey:
    def __init__(self, attr, ref_tab, ref_attr):
        self.attribute = attr
        self.referenced_table = ref_tab
        self.referenced_attribute = ref_attr
    #change the properties to string for easier generation of fk's as well as mem. efficiency
    #the fk doesn't need to be aware of the containing table

    # def set_table(self, table):
    #     self.table = table
    #
    # def set_attribute(self, attribute):
    #     self.attribute = attribute
    #
    # def set_ftable(self, table):
    #     self.fTable = table
    #
    # @property
    # def get_table(self):
    #     return self.table
    #
    # @property
    # def get_attribute(self):
    #     return self.attribute
    #
    # @property
    # def get_ftable(self):
    #     return self.fTable