__author__ = 'Maira'
import xml.etree.ElementTree as elementTree
from dbnormalizer.core.table.schema import Schema
from dbnormalizer.core.table.Table import Table
from dbnormalizer.core.table.Attr import Attribute
from dbnormalizer.core.table.FD import FD
import re

# this class parses an XML file and returns the schema for the normalizer.
# If the XML file is not on the correct format, the system will trough an exception
class XMLImport:
    def __init__(self, xml_data, test=False):
        self.test = test
        self.xml_data = xml_data
        self.fileStructure = ''
        self.schema = {}
        self.tables = []
        self.attributes = {}
        self.intermediateTables = {}

    def readfile(self):
        if self.test:
            self.fileStructure = elementTree.parse(self.xml_data)
        else:
            self.fileStructure = elementTree.fromstring(self.xml_data)

    def init_objects(self):
        self.readfile()
        self.init_schema()
        self.init_tables()
    
    def get_schema(self):
        return self.schema

    def init_schema(self):
        if self.test:
            root = self.fileStructure.getroot()
        else:
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
                t['attributes'] = self.init_attributes(table, table_name)
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

    def init_attributes(self, table, table_name):
        attr = set()
        try:
            for attributes in table.findall('.//attributes'):
                for a in attributes.findall('.//attribute'):
                    attrs = a.text.replace(')', '')
                    attrs = attrs.replace('(', '')
                    attrs = attrs.split(',')
                    for at in attrs:
                        at = Attribute(at)
                        attr.add(at)
            return attr
        except Exception as e:
            print('init_attributes ' + str(e))

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

    def handle_intermediate_tables_fds(self, lhs, rhs, table_name):
        lhs_list = []
        rhs_list = []
        add_to_main_table = True
        for attribute in lhs.findall('.//attribute'):
            a = attribute.text
            lhs_list.append(a)
            if a not in self.attributes[table_name]:
                add_to_main_table = False
        for attribute in rhs.findall('.//attribute'):
            a = attribute.text
            rhs_list.append(a)
            if a not in self.attributes[table_name]:
                add_to_main_table = False

        if not add_to_main_table:
            attrs = lhs_list + rhs_list
            for inttable in self.intermediateTables[table_name]:
                common_elem = list(set(inttable) & set(attrs))
                print(common_elem)
                if len(common_elem) > 0:
                    print('table: '+str(inttable)+' attrs: '+str(attrs))

            #print(attrs)

        #print(str(lhs_list)+'->'+str(rhs_list))

        return add_to_main_table

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

    def treat_attr(self, attr, table_name):
        t = attr.split(',')
        if len(t) == 1:
            return attr
        self.getIntermediateTables(t, table_name)
        return False

    def getIntermediateTables(self, t, table_name):
        tables = []
        attr = []
        added_elem = True
        for a in t:
            if '(' in a:
                a = a.replace('(', '')
                if not added_elem:
                    tables.append(attr)
                added_elem = False
                attr = [a]
            elif ')' in a:
                a = a.replace(')', '')
                attr.append(a)
                tables.append(attr)
                attr = []
                added_elem = True

            else:
                added_elem = False
                attr.append(a)

        self.intermediateTables[table_name] = []
        i = 0
        for t in tables:
            tb = Table(table_name+str(i))
            tb_at = []
            self.intermediateTables[table_name].append(t)
            for a in t:
                at = Attribute(a)
                tb_at.append(at)
            tb.set_attributes(tb_at)
            i += 1
            self.tables.append(tb)

#test = XMLImport('/Users/mairamachadoladeira/PycharmProjects/adb_project/examples/presentation_example2.xml', True)
#test.init_objects()
#schema = test.get_schema()
#tables = schema.get_tables()
#for t in tables:
    #print(t.get_attributes)