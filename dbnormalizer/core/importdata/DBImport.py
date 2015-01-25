import dbnormalizer
from dbnormalizer.core.table.schema import Schema
from dbnormalizer.core.table.Table import Table
from dbnormalizer.core.table.Attr import Attribute
from dbnormalizer.core.table.FD import FD

__author__ = 'Iva'

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import reflection


class DBImport:
    """ class used to import the db metadata from a postgresql database
    """
    def __init__(self, url, username, password, dbschema, database):
        self.username = username
        self.password = password
        self.database = database
        self.schema = dbschema
        self.engine = create_engine('postgresql://' + username + ':' + password + '@'+url+'/' + database)
        self.connection = self.engine.connect()
        self.metadata = MetaData(self.engine, reflect=True, schema=self.schema)
        self.inspector = reflection.Inspector.from_engine(self.engine)
        self.connection.close()

    def map_tables(self):
        mapped = Schema(self.schema)
        for table_name in self.inspector.get_table_names(schema=self.schema):
            new_table = Table(table_name)
            columns = self.inspector.get_columns(table_name, self.schema)
            attributes = []
            for c in columns:
                attr_new = Attribute(c['name'])
                attr_new.set_type(c['type'])
                attributes.append(attr_new)
            new_table.set_attributes(attributes)
            primary_key = self.inspector.get_pk_constraint(table_name, self.schema)
            fds = self.construct_fd_from_pk(primary_key['constrained_columns'], attributes)
            new_table.fds = fds
            mapped.add_table(new_table)
        return mapped

    def construct_fd_from_pk(self, primary, attributes):
        fds = []
        prim = []
        for col in primary:
            att = Attribute(col)
            prim.append(att)
        for att in attributes:
            same_att = False
            if isinstance(prim, list):
                for part in prim:
                    if part.get_name == att.get_name:
                        same_att = True
            elif lhs.get_name == att.get_name:
                same_att = True

            if not same_att:
                lhs = prim
                rhs = [att]
                fd = FD(lhs=lhs, rhs=rhs)
                fds.append(fd)
        return fds

    def print_table_info(self):
        for table_name in self.inspector.get_table_names(schema=self.schema):
            print("Table: " + table_name)
            columns = self.inspector.get_columns(table_name, self.schema)
            for c in columns:
                print("\tColumn: " + c['name'])
            primary_key = self.inspector.get_pk_constraint(table_name, self.schema)
            print("\tPrimary key is: ", primary_key['constrained_columns'])
            fk = self.inspector.get_foreign_keys(table_name, self.schema)
            print("\tForeign keys:  ", fk)


# proba = DBImport(username='postgres', password='postgres', database='adb_test', dbschema='test')
# proba.print_table_info()
# maped = proba.map_tables()

