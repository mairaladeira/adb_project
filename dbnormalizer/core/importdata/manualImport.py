__author__ = 'Maira'
from dbnormalizer.core.table.schema import Schema
from dbnormalizer.core.table.Table import Table
from dbnormalizer.core.table.Attr import Attribute
from dbnormalizer.core.table.FD import FD


# this class parses an XML file and returns the schema for the normalizer.
# If the XML file is not on the correct format, the system will trough an exception
class ManualImport:
    def __init__(self, data):
        self.data = data
        self.schema = {}
        self.set_schema()
        return

    def get_schema(self):
        return self.schema

    def set_schema(self):
        schema_name = self.data['Schema']
        self.schema = Schema(schema_name)
        tables = self.data['Tables']
        for t in tables:
            table = self.set_table(t)
            self.schema.add_table(table)

    @staticmethod
    def set_table(table):
        name = table['name']
        t = Table(name)
        fds = table['fds']
        attributes = table['attributes']
        attributes_list = []
        fds_list = []
        for attr in attributes:
            attribute = Attribute(attr)
            attributes_list.append(attribute)
        for fd in fds:
            lhs_list = []
            rhs_list = []
            for a in attributes_list:
                attr_name = a.get_name
                for lhs in fd['lhs']:
                    if lhs == attr_name:
                        lhs_list.append(a)
                for rhs in fd['rhs']:
                    if rhs == attr_name:
                        rhs_list.append(a)

            fd_elem = FD(lhs_list, rhs_list)
            fds_list.append(fd_elem)

        t.set_attributes(attributes_list)
        t.set_fds(fds_list)
        return t


#test_data = {'Schema': 'Test', 'Tables': [{'fds': [{'lhs': ['attr1'], 'rhs': ['attr2']}, {'lhs': ['attr1'], 'rhs': ['attr3']}, {'lhs': ['attr3'], 'rhs': ['attr2']}], 'name': 'Test1', 'attributes': ['attr1', 'attr2', 'attr3']}]}
#mi = ManualImport(test_data)
#schema = mi.get_schema()
#print(schema)