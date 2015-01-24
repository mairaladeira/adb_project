__author__ = 'Maira'
import xml.etree.ElementTree as elementTree
from dbnormalizer.core.table.schema import Schema
from dbnormalizer.core.table.Table import Table
from dbnormalizer.core.table.Attr import Attribute
from dbnormalizer.core.table.FD import FD


# this class parses an XML file and returns the schema for the normalizer.
# If the XML file is not on the correct format, the system will trough an exception
class XMLImport:
    def __init__(self, xml_data):
        self.xml_data = xml_data
        self.fileStructure = ''
        self.schema = {}
        self.tables = []
        self.attributes = {}

    def readfile(self):
        self.fileStructure = elementTree.fromstring(self.xml_data)

    def init_objects(self):
        self.readfile()
        self.init_schema()
        self.init_tables()
    
    def get_schema(self):
        return self.schema

    def init_schema(self):
        root = self.fileStructure
        for s in root.findall('schema'):
            self.schema = Schema(s.get('name'))
            self.fileStructure = s

    def init_tables(self):
        s = self.fileStructure
        t = {}
        try:
            for table in s.findall('.//table'):
                table_name = table.get('name')
                t['attributes'] = self.init_attributes(table)
                self.attributes[table_name] = []
                for attr in t['attributes']:
                    self.attributes[table_name].append(attr.get_name)
                t['fds'] = self.init_fds(table, table_name)
                tb = Table(table_name)
                tb.set_attributes(t['attributes'])
                tb.set_fds(t['fds'])
                self.tables.append(tb)
                self.schema.add_table(tb)
        except Exception as e:
            print('init_tables')
            print(e)

    @staticmethod
    def init_attributes(table):
        attr = set()
        try:
            for attributes in table.findall('.//attributes'):
                for a in attributes.findall('.//attribute'):
                    a = Attribute(a.text)
                    attr.add(a)
            return attr
        except Exception as e:
            print('init_attributes' + str(e))

    def check_fds_attributes(self, table, table_name):
        attr = []
        try:
            for attribute in table.findall('.//attribute'):
                a = Attribute(attribute.text)
                if attribute.text in self.attributes[table_name]:
                    attr.append(a)
                else:
                    print('All the fds MUST be composed of table attributes!')
            return attr
        except Exception as e:
            print('init_attributes' + str(e))

    def init_fds(self, table, table_name):
        fds = []
        try:
            for fd in table.findall('.//fd'):
                fds.append(FD(self.check_fds_attributes(fd.find('lhs'), table_name), self.check_fds_attributes(fd.find('rhs'), table_name)))
            if len(fds) == 0:
                print('No functional dependency found! please add the functional dependencies!')
            return fds
        except Exception as e:
            print('get function dependencies exception: '+ str(e))