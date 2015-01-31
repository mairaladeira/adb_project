__author__ = 'Iva'

# import xml.etree.ElementTree as elemTree
#
# root = elemTree.Element("root")
# doc = elemTree.SubElement(root, "doc")
#
# elemTree.SubElement(doc, "field1", name="blah").text = "some value1"
# elemTree.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
#
# tree = elemTree.ElementTree(root)
# tree.write("filename.xml")
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring
from xml.dom import minidom


class XMLExport:

    def __init__(self, schema):
        self.schema = schema
        self.xml = ''

    def generate_xml(self):
        try:
            conf = Element('configuration')
            schema = SubElement(conf, 'schema', {'name': self.schema.name})
            table_info = SubElement(schema, 'tableInfo')
            #schema.text = self.schema.name
            for tab in self.schema.get_tables():
                table = SubElement(table_info, 'table', {'name': tab.name})
                attributes = SubElement(table, 'attributes')
                for attr in tab.get_attributes:
                    attribute = SubElement(attributes, 'attribute')
                    attribute.text = attr.name
                fds = SubElement(table, 'fds')
                for fd_s in tab.get_fds:
                    fd = SubElement(fds, 'fd')
                    lhs = SubElement(fd, 'lhs')
                    for atr_lhs in fd_s.get_lhs:
                        att_fd = SubElement(lhs, 'attribute')
                        att_fd.text = atr_lhs.name
                    rhs = SubElement(fd, 'rhs')
                    for atr_rhs in fd_s.get_rhs:
                        att_fd = SubElement(rhs, 'attribute')
                        att_fd.text = atr_rhs.name
            self.xml = self.prettify(conf)
            return self.xml
            #filename = "xml_mapping_" + self.schema.name + ".xml"
            #xml_file = open(filename, mode='w')
            #xml_file.write(self.xml)
            #xml_file.close()
            #import os.path
            #import inspect
            #path_to_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            #path_to_file = path_to_dir + "\\" + filename
            #return path_to_file
        except Exception as e:
            print('Error creating new xml file: ' + str(e))
            self.error = str(e.args[0])


    def prettify(self,elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

#
# from dbnormalizer.core.importdata.XMLImport import XMLImport
#
# test = XMLImport(r'C:\adb_project\examples\test.xml',True)
# test.init_objects()
# schema = test.get_schema()
# ex = XMLExport(schema)
# xml = ex.generate_xml()
# print(xml)

