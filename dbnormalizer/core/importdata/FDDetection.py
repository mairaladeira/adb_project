__author__ = 'Iva'
from dbnormalizer.core.table.Table import Table
from dbnormalizer.core.table.FD import FD
from dbnormalizer.core.table.Attr import Attribute
from dbnormalizer.core.importdata.StrippedPartition import StrippedPartition
from dbnormalizer.core.importdata.CandidateInfo import CandidateInfo


class FDDetection:
    def __init__(self, engine, schema_name, table):
        self.engine = engine
        self.table = table
        self.schema_name = schema_name
        self.table_full_name = self.schema_name + "." + str(table.name)
        self.partitions = []


    def setup_table(self):
        conn = self.engine.connect()
        partitions=[]
        attr_list = self.table.get_attribute_string_list_combined()

        for column in attr_list:
            res = conn.execute("select " + column + " from " + self.table_full_name + " order by " + attr_list[0])
            if res:
                partition = StrippedPartition(column, res)
                self.partitions.append(partition)
        return self.partitions

    def find_fds(self):
        fd_list = []
        for part in self.partitions:
            #set_part = self.construct_set_from_part(part.column)
            for attr in self.table.get_attribute_string_list_no_pk():
                set_attr = set(attr)
                if attr not in part.column_set:
                    union = part.column_set | set_attr
                    union_part = self.find_partition_by_set(union)
                    if union_part:
                        if part.no_equivalence_classes == union_part.no_equivalence_classes:
                            lhs =[]
                            for col in part.column_set:
                                lhs.append(Attribute(col))
                            rhs = Attribute(attr)
                            fd_list.append(FD(lhs, rhs))
        return fd_list

    def find_partition_by_set(self, part_set):
        for part in self.partitions:
            if part_set == part.column_set:
                return part




    # def construct_set_from_str(self, str_column):
    #     list_split = str_column.split(sep = ',')
    #     return set(list_split)
