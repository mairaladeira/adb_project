import dbnormalizer
from dbnormalizer.core.table.schema import Schema
from dbnormalizer.core.table.Table import Table
from dbnormalizer.core.table.Attr import Attribute
from dbnormalizer.core.table.FD import FD

__author__ = 'Iva'

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import reflection
from dbnormalizer.core.table.FKey import FKey
from dbnormalizer.core.importdata.FDDetection import FDDetection


class DBImport:
    """ class used to import the db metadata from a postgresql database
    """
    def __init__(self, url, username, password, dbschema, database, check_fds_from_data=True):
        self.username = username
        self.password = password
        self.database = database
        self.schema = dbschema
        self.engine = None
        self.connection = None
        self.metadata = None
        self.inspector = None
        self.error = None
        #self.fds_data = None
        self.check_fds_from_data = check_fds_from_data
        try:
            self.engine = create_engine('postgresql://' + username + ':' + password + '@'+url+'/' + database)
            self.connection = self.engine.connect()
            self.metadata = MetaData(self.engine, reflect=True, schema=self.schema)
            self.inspector = reflection.Inspector.from_engine(self.engine)
            self.connection.close()
        except Exception as e:
            print('Error with database connection: ' + str(e))
            self.error = str(e.args[0])

    def get_error(self):
        return self.error

    def map_tables(self):
        mapped = Schema(self.schema)
        mapped.import_from_db = True
        for table_name in self.inspector.get_table_names(schema=self.schema):
            new_table = Table(table_name)
            columns = self.inspector.get_columns(table_name, self.schema)
            primary_key = self.inspector.get_pk_constraint(table_name, self.schema)
            foreign_import = self.inspector.get_foreign_keys(table_name, self.schema)
            attributes = []
            for c in columns:
                attr_new = Attribute(c['name'])
                attr_new.set_type(c['type'])
                attributes.append(attr_new)
                if c['name'] in primary_key['constrained_columns']:
                    new_table.pk.append(c['name'])
                elif c['name'] in foreign_import:
                    new_table.imported_fk.append(c['name'])
            new_table.set_attributes(attributes)
            if primary_key['constrained_columns']:
                fds = self.construct_fd_from_pk(primary_key['constrained_columns'], attributes)
                new_table.fds = fds
            for fk in foreign_import:
                new_table.imported_fk.append(FKey(fk['constrained_columns'], fk['referred_table'], fk['referred_columns']))
            self.connection = self.engine.connect()
            result = self.connection.execute("select count(*) as count from " + self.schema + "." + new_table.name)
            for row in result:
                new_table.db_row_count = row['count']
            if self.check_fds_from_data:
                fds_detect = FDDetection(self.engine, self.schema, new_table)
                fds_detect.setup_table()
                fds_data = fds_detect.find_fds()
                for fd in fds_data:
                    new_table.fds.append(fd)
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

    def check_fds_hold(self, fds, table_name):
        fd_hold = []
        fd_not_hold = []
        holds = False
        if isinstance(fds, list):
            for one_fd in fds:
                holds = self.check_fd_hold(one_fd, table_name)
                if holds:
                    fd_hold.append(one_fd)
                else:
                    fd_not_hold.append(one_fd)
        else:
            holds = self.check_fd_hold(fds, table_name)
            if holds:
                fd_hold.append(fds)
            else:
                fd_not_hold.append(fds)
        fds_situation = {'hold': fd_hold, 'not_hold': fd_not_hold}
        return fds_situation

    def check_fd_hold(self, one_fd, table_name):
        try:
            group_left = []
            lhs = one_fd.get_lhs
            if isinstance(lhs, list):
                for att in lhs:
                    group_left.append(str(att.get_name))
            else:
                group_left.append(str(lhs.get_name))

            group_right = []
            rhs = one_fd.get_rhs
            if isinstance(rhs, list):
                for att in rhs:
                    group_right.append(str(att.get_name))
            else:
                group_right.append(str(rhs.get_name))

            string1 = ", ".join(str(x) for x in group_left)
            string2 = ", ".join(str(x) for x in group_right)

            query = "select count(*) as count from (select distinct " + string1 + ", " \
                    + string2 + " from " + str(self.schema) + "." + str(table_name) \
                    + ") as temptable group by " + string1 + " having count(*) > 1"

            #print(query)
            self.connection = self.engine.connect()
            result = self.connection.execute(query)
            self.connection.close()
            if result.rowcount == 0:
                return True #functional dependecy holds
            else:
                return False
        except Exception as e:
            print('Error with query, check if fd is good: ' + str(e))
            self.error = str(e.args[0])

# from dbnormalizer.core.importdata.StrippedPartition import StrippedPartition
# proba = DBImport(username='postgres', password='postgres', url='localhost:5432', database='tane', dbschema='public', check_fds_from_data=True)
# conn = proba.engine.connect()
# maped = proba.map_tables()
# diction = proba.fds_data
# for fd in diction:
#     print(", ".join( str(attr.name) for attr in fd.lhs) + "->" + ", ".join( str(attr.name) for attr in fd.rhs))

