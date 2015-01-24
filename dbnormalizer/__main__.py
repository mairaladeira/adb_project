import os
import subprocess

__author__ = 'Maira'

##from dbnormalizer.core.importdata.XMLImport import XMLImport

#test = XMLImport('/Users/mairamachadoladeira/PycharmProjects/adb_project/examples/test.xml')
#test.init_objects()
#schema = test.get_schema()
#for table in schema.get_tables():
   # print(table.get_name)

# code to run an example

# from dbnormalizer.core.importdata.DBImport import DBImport
# username = password = 'postgres'
# database = 'adb_test'
# schema = 'test'
# im = DBImport(username, password, database, schema)
# im.map_tables()

file_path = os.path.abspath(os.path.dirname(__file__))+'/web/web.py'
try:
    subprocess.call(["python3", file_path])
except OSError as e:
    subprocess.call(["python", file_path])