__author__ = 'Maira'

import sqlalchemy
import pyparsing

from dbnormalizer.core.importdata.XMLImport import XMLImport


test = XMLImport('/Users/mairamachadoladeira/PycharmProjects/adb_project/examples/test.xml')
test.readfile()