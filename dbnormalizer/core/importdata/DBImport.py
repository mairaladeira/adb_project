__author__ = 'Iva'


from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import reflection
from dbnormalizer.core.table import Schema, Table, Attr

# code to run an example
# username = password = 'adbproject'
# database = 'adb_test'
# schema = 'test'
# im = DBImport(username, password, database, schema)
# im.print_table_info()

class DBImport:
    """ class used to import the db metadata from a postgresql database
    """
    def __init__(self, username, password, database, dbschema):
        self.username = username
        self.password = password
        self.database = database
        self.schema = dbschema
        self.engine = create_engine('postgresql://' + username + ':' + password + '@localhost/' + database)
        self.connection = self.engine.connect()
        self.metadata = MetaData(self.engine, reflect=True, schema=self.schema)
        self.inspector = reflection.Inspector.from_engine(self.engine)
        self.connection.close()

    def map_tables(self):
        mapped = Schema(self.schema)
        for table_name in self.inspector.get_table_names(schema=self.schema):
            new_table = Table(table_name)
            columns = self.inspector.get_columns(table_name, self.schema)
            for c in columns:
                new_table.add_columns(c['name'])
            mapped.add_table(Table(table_name))
        return mapped

    def print_table_info(self):
        for table_name in self.inspector.get_table_names(schema=self.schema):
            print("Table: " + table_name)
            columns = self.inspector.get_columns(table_name, self.schema)
            for c in columns:
                print("\tColumn: " + c['name'])
            primary_key = self.inspector.get_pk_constraint(table_name, self.schema)
            print("\tPrimary key is: ", primary_key['constrained_columns'])
            fk = self.inspector.get_foreign_keys(table_name, self.schema)
            print("\tForeign keys: ", fk)


