__author__ = 'Maira'
import xml.etree.ElementTree as elementTree


# this class parses an XML file and returns the schema for the normalizer.
# If the XML file is not on the correct format, the system will trough an exception
class XMLImport:
    def __init__(self, file_name):
        self.file = file_name
        self.fileStructure = ''
        self.schemaName = ''
        self.tables = {}

    def readfile(self):
        self.fileStructure = elementTree.parse(self.file)
        root = self.fileStructure.getroot()
        self.get_schema(root)
        print(self.tables)

    def get_schema(self, root):
        for schema in root.findall('schema'):
            self.schemaName = schema.get('name')
            self.get_tables(schema)

    def get_tables(self, schema):
        t = {}
        try:
            for table in schema.findall('.//table'):
                t['attributes'] = self.get_attributes(table)
                t['fds'] = self.get_functional_dependencies(table)
                self.tables[table.get('name')] = t
        except Exception as e:
            print('get_tables')
            print(e)

    @staticmethod
    def get_attributes(table):
        attr = set()
        try:
            for attribute in table.findall('.//attribute'):
                attr.add(attribute.text)
            return attr
        except Exception as e:
            print('get_attributes' + e)


    def get_functional_dependencies(self, table):
        dependency = {}
        fds = {}
        i = 0
        try:
            for fd in table.findall('.//fd'):
                dependency['left'] = self.get_attributes(fd.find('left'))
                dependency['right'] = self.get_attributes(fd.find('right'))
                fds[i] = dependency
                i += 1
            if 0 == i:
                print('problem')
            return fds
        except Exception as e:
            print('get_attributes')
            print(e)