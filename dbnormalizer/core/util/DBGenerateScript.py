__author__ = 'Iva'

from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, ForeignKey,ForeignKeyConstraint, Column, Integer, String
from dbnormalizer.core.table.schema import Schema

class DBGenerateScript:
    """class used to generate SQL scripts for normalizing the database"""

    def __init__(self, norm_schema, old_schema):
        self.normalized_schema = norm_schema
        self.old_schema = old_schema
        self.script = ''
        self.engine = create_engine('postgresql://adb:adb@doesntmatter/base', strategy='mock', executor= lambda sql, *multiparams, **params: print(sql, ";"))
        self.metadata_new = MetaData(schema=self.normalized_schema.name)
        self.metadata_old = MetaData(schema=self.old_schema.name)

    def generate_script(self):
        #generate the DDL statements to create new tables and add foreign keys
        for tab in self.normalized_schema.get_tables():
            table = Table(tab.get_name, self.metadata_new)
            for attr in tab.get_attributes:
                is_pk = attr.get_name in tab.pk
                col = Column(attr.get_name, attr.get_type, primary_key=is_pk)
                table.append_column(col)
            for fk in tab.f_keys:
                for ref in fk.referenced_attribute:
                    name = []
                    name.append(fk.referenced_table + '.' + ref)
                    fkcon = ForeignKeyConstraint(columns=fk.attribute, refcolumns=name)
                    table.append_constraint(fkcon)

        #DDL preserve foreign keys
        for tab_old in self.old_schema.get_tables():
            for fk in tab_old.imported_fk:
                # for attr_old in tab_old.get_attributes:
                #     for attr_new in tab_new.get_attributes:
                #         if attr_old.name == attr_new.name:
                for ref in fk.referenced_attribute:
                    name = []
                    name.append(fk.referenced_table + '.' + ref)
                    fkcon = ForeignKeyConstraint(columns=fk.attribute, refcolumns=name, use_alter=True, name='sdd')
                    table.append_constraint(fkcon)

        #dropping the old tables
        for tab in self.old_schema.get_tables():
            table = Table(tab.get_name, self.metadata_old)

        script1 = str(self.metadata_new.create_all(self.engine))
        script2 = str(self.metadata_old.drop_all(self.engine))
        self.script = script1 + script2

        return self.script

# node = Table('node', metadata,
#     Column('node_id', Integer, primary_key=True),
#     Column('primary_element', Integer,
#         ForeignKey('element.element_id', use_alter=True, name='fk_node_element_id')
#     )
# )

# metadata = MetaData()
# element = Table('element', metadata,
#         ForeignKeyConstraint(
#         ['parent_node_id'],
#         ['node.node_id'],
#         use_alter=True,
#         name='fk_element_parent_node_id'))
# engine = create_engine('postgresql://adb:adb@doesntmatter/base', strategy='mock', executor= lambda sql, *multiparams, **params: print (sql, ";"))
# from dbnormalizer.core.importdata.DBImport import DBImport
# proba = DBImport(username='postgres', password='postgres', url='localhost:5432', database='adb_test', dbschema='test')
# maped = proba.map_tables()
# for tab in maped.get_tables():
#     tab.f_keys = tab.imported_fk
# gen = DBGenerateScript(maped, maped)
# script = gen.generate_script()
# print(script)