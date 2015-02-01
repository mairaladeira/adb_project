__author__ = 'Iva'

from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData
from sqlalchemy.schema import CreateTable, DropTable, Constraint
from sqlalchemy import Table, ForeignKey, ForeignKeyConstraint, Column, Integer, String
from dbnormalizer.core.table.schema import Schema

class DBGenerateScript:
    """class used to generate SQL scripts for normalizing the database"""

    def __init__(self, norm_schema, old_schema, username, password, url, database):
        self.normalized_schema = norm_schema
        self.old_schema = old_schema
        self.script = ''
        self.sql_list = []
        def dump(sql, *multiparams, **params):
            return self.sql_list.append(str(sql.compile(dialect=self.engine.dialect)).strip()+';\n')
        self.engine = create_engine('postgresql://' + username + ':' + password + '@'+url+'/' + database, strategy='mock',executor=dump)
                                    #executor= lambda sql, *multiparams, **params: print(sql, ";"))
        self.metadata_new = MetaData(schema=self.normalized_schema.name)
        self.metadata_old = MetaData(schema=self.old_schema.name)

    def generate_DDL_create_new(self):
        #generate the DDL statements to create new tables and add foreign keys
 #       script_new = ''
        #ensure schema consistency
        for tab in self.normalized_schema.get_tables():
            for attr in tab.get_attributes:
                if attr.type == "":
                    for tab_old in self.old_schema.get_tables():
                        attr.type = tab_old.get_attribute_by_name(attr.get_name).type
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
        # for tab_old in self.old_schema.get_tables():
        #     for fk in tab_old.imported_fk:
        #         # for attr_old in tab_old.get_attributes:
        #         #     for attr_new in tab_new.get_attributes:
        #         #if attr_old.name == attr_new.name:
        #             for ref in fk.referenced_attribute:
        #                 name = []
        #                 name.append(fk.referenced_table + '.' + ref)
        #                 fkcon = ForeignKeyConstraint(columns=fk.attribute, refcolumns=name, use_alter=True, name= ref+'_'+tab_old.name + '_fk')
        #                 table.append_constraint(fkcon)
                    #print(str(fkcon.compile(self.engine)))


        #script_new += str(CreateTable(table).compile(self.engine))+';'
        self.metadata_new.create_all(self.engine, checkfirst=False)
#        return script_new

    def generate_DDL_drop_old(self):
        #dropping the old tables
  #      script_old = ''
        for tab in self.old_schema.get_tables():
            table = Table(tab.get_name, self.metadata_old)
            #script_old += str(DropTable(table).compile(self.engine))+';'
        self.metadata_old.drop_all(self.engine, checkfirst=False)
   #     return script_old

    def generate_DML_old_to_new(self):
        from sqlalchemy.sql import table, column
        from sqlalchemy.sql.expression import select
        for tab in self.normalized_schema.get_tables():
            ins_into = table(self.normalized_schema.name + '.'+ tab.get_name)
            for tab_old in self.old_schema.get_tables():
                sel_from = table(self.old_schema.name + '.'+ tab_old.name)
            col_list = []
            col_string = ''
            for attr in tab.get_attributes:
                col_list.append(attr.get_name)
                col_string += ' '+attr.get_name
                col = column(attr.get_name)
                ins_into.append_column(col)
            insert_statement = str(ins_into.insert().from_select(col_list, select(columns=col_list, from_obj=sel_from,distinct=True)))
        #
        # t1 = table('t1', column('a'), column('b'))
        # t2 = table('t2', column('x'), column('y'))
        # script3 = str(t1.insert().from_select(['a', 'b'], t2.select().where(t2.c.y == 5)))
            self.sql_list.append('\n\n'+ insert_statement + ';\n')


    def generate_script(self):
        self.generate_DDL_create_new()
        self.generate_DML_old_to_new()
        self.generate_DDL_drop_old()
        for q in self.sql_list:
            self.script += q


        return self.script

# from dbnormalizer.core.importdata.DBImport import DBImport
# from dbnormalizer.core.table.Attr import Attribute
# from dbnormalizer.core.table.FD import FD
# from dbnormalizer.core.normalizer.NF import NF
# from dbnormalizer.core.normalizer.normalizer import Normalizer
# from dbnormalizer.core.table.schema import Schema
# proba = DBImport(username='postgres', password='postgres', url='localhost:5432', database='adb_test', dbschema='test')
# maped_old = proba.map_tables()
# table = maped_old.get_table_by_name("new")
# a1 = Attribute("anew")
# a2 = Attribute("cnew")
# lhs = []
# lhs.append(a1)
# rhs = []
# rhs.append(a2)
# table.add_fd(FD(lhs,rhs))
# nf = NF(table)
# current_nf = nf.determine_nf()
# normalization = Normalizer(nf)
# normalization.decomposition()
# schema  = Schema("new")
# table_bcnf = normalization.get_new_tables_bcnf()
# for tab in table_bcnf:
#     schema.add_table(tab)
# username=password= 'postgres'
# url = 'localhost:5432'
# database = 'adb_test'
# gen = DBGenerateScript(schema, maped_old, username, password, url, database)
# script = gen.generate_script()
# print(script)
# for q in gen.sql_list:
#     print(q)

# from sqlalchemy.sql import table, column
# t1 = table('t1', column('a'), column('b'))
# t2 = table('t2', column('x'), column('y'))
# script = str(t1.insert().from_select(['a', 'b'], t2.select().where(t2.c.y == 5)))
# print(script)
#
# def dump(sql, *multiparams, **params):
#     return sql.compile(dialect=engine.dialect)
# engine = create_engine('postgresql://', strategy='mock', executor=dump)
# metadata.create_all(engine, checkfirst=False)