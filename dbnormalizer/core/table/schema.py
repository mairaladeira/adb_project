__author__ = 'Maira'


class Schema:
    def __init__(self, name):
        self.name = name
        self.tables = []
        self.import_from_db = False

    @property
    def get_name(self):
        return self.name

    def add_table(self, table):
        self.tables.append(table)

    def get_tables(self):
        return self.tables

    def get_table_fds(self, table_name):
        for table in self.tables:
            if table.get_name == table_name:
                return table.get_fds
        return None

    def get_table_attributes(self, table_name):
        for table in self.tables:
            if table.get_name == table_name:
                return table.get_attributes
        return None

    def get_table_by_name(self, table_name):
        for table in self.tables:
            if table.get_name == table_name:
                return table
        return None

