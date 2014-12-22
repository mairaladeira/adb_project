__author__ = 'Maira'

from dbnormalizer.core.importdata.XMLImport import XMLImport

test = XMLImport('/Users/mairamachadoladeira/PycharmProjects/adb_project/examples/test.xml')
test.init_objects()
schema = test.get_schema()
for table in schema.get_tables():
    print(table.get_name)