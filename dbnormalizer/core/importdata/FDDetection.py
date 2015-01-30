__author__ = 'Iva'
from dbnormalizer.core.table.Table import Table
from dbnormalizer.core.importdata.StrippedPartition import StrippedPartition


class FDDetection:
    def __init__(self, engine, schema_name, table):
        self.engine = engine
        self.table = table
        self.schema_name = schema_name
        self.table_full_name = self.schema_name + "." + str(table.name)

    def setup_table(self):
        conn = self.engine.connect()
        partitions=[]
        attr_list = self.table.get_attribute_string_list()
        for column in attr_list:
            res = conn.execute("select " + column + " from " + self.table_full_name + " order by " + attr_list[0])
            if res:
                partition = StrippedPartition(column, res)
                partitions.append(partition)
        return partitions


    def get_data(self):
        connection = self.engine.connect()
        result = connection.execute("select * from " + self.table_full_name)
        return result


