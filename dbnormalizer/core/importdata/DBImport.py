__author__ = 'Iva'


from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import reflection

# username = password = 'adbproject'
# database = 'dbpython'
# im = DBImport(username, password, database)
# im.print_table_info()

class DBImport:
    """ class used to import the db metadata from a postgresql database
    """
    def __init__(self, username, password, database):
        self.username = username
        self.password = password
        self.database = database
        self.engine = create_engine('postgresql://' + username + ':' + password + '@localhost/' + database)
        self.connection = self.engine.connect()
        self.metadata = MetaData(self.engine, reflect=True)
        self.inspector = reflection.Inspector.from_engine(self.engine)
        self.connection.close()

    def print_table_info(self):
        for table_name in self.inspector.get_table_names():
            print("Table: " + table_name)
            columns = self.inspector.get_columns(table_name)
            for c in columns:
                print("\tColumn: " + c['name'])
            primary_key = self.inspector.get_pk_constraint(table_name)
            print("\tPrimary key is: ", primary_key['constrained_columns'])
            fk = self.inspector.get_foreign_keys(table_name)
            print("\tForeign keys: ", fk)