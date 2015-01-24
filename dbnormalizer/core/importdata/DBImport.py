__author__ = 'Iva'


from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import reflection

# code to run an example
# username = password = 'adbproject'
# database = 'adb_test'
# schema = 'test'
# im = DBImport(username, password, database, schema)
# im.print_table_info()

class DBImport:
    """ class used to import the db metadata from a postgresql database
    """
    def __init__(self, username, password, database, schema):
        self.username = username
        self.password = password
        self.database = database
        self.schema = schema
        self.engine = create_engine('postgresql://' + username + ':' + password + '@localhost/' + database)
        self.connection = self.engine.connect()
        self.metadata = MetaData(self.engine, reflect=True, schema=self.schema)
        self.inspector = reflection.Inspector.from_engine(self.engine)
        self.connection.close()

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