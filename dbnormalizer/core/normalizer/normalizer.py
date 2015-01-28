__author__ = 'Mehreeen'
from dbnormalizer.core.table.FD import FD
from dbnormalizer.core.table.Table import Table


class Normalizer:
    def __init__(self, normal_form):
        self.nf = normal_form

        # fds for the normalization
        self.fds = self.get_fds_union()

        self.new_tables = []

    def get_new_tables(self):
        return self.new_tables

    """
    Union of fds
    Example:
        A -> B
        A -> C

        returns
        A -> BC
    """
    def get_fds_union(self):
        fds = self.nf.calculate_mincover()
        united_fds = []
        lhs_fds = []
        i = 0
        for fd_1 in fds:
            lhs_1_name = [l.get_name for l in fd_1.get_lhs]
            j = 0
            for fd_2 in fds:
                lhs_2_name = [l.get_name for l in fd_2.get_lhs]
                if j >= i:
                    if lhs_1_name == lhs_2_name and j > i:
                        lhs_fds.remove(lhs_1_name)
                        united_fds.remove(fd_1)
                        lhs_fds.append(lhs_1_name)
                        rhs = fd_1.get_rhs + fd_2.get_rhs
                        new_fd = FD(fd_1.get_lhs, rhs)
                        united_fds.append(new_fd)
                    else:
                        if lhs_1_name not in lhs_fds:
                            united_fds.append(fd_1)
                            lhs_fds.append(lhs_1_name)
                j += 1
            i += 1
        return united_fds

    """
    decomposition of a table up to 3NF
    Return the new tables
    """
    def decomposition(self):
        generated_tables = {}
        generated_tables_aux = []
        new_tables = []
        checked_attributes = set()
        old_table = self.nf.get_table()
        i = 0

        #Create a new table for each FD after the union operation
        for fd in self.fds:
            lhs = fd.get_lhs
            rhs = fd.get_rhs
            t_attr = lhs + rhs
            generated_tables[old_table.get_name+'_'+str(i + 1)] = {'attr': t_attr, 'fds': [fd]}
            generated_tables_aux.append(t_attr)
            for a in t_attr:
                checked_attributes.add(a.get_name)
            i += 1
        i = 0

        #check if any of the fds is contained on the set of attributes of fds
        #example: B->D, D->E and BD->E: Table BDE should eliminate the BD and DE tables
        for t_1 in generated_tables_aux:
            j = 0
            attr_1 = [a.get_name for a in t_1]
            for t_2 in generated_tables_aux:
                attr_2 = [a.get_name for a in t_2]
                if set(attr_1) < set(attr_2):
                    generated_tables[old_table.get_name+'_'+str(j + 1)]['fds'].append(generated_tables[old_table.get_name+'_'+str(i + 1)]['fds'])
                    del generated_tables[old_table.get_name+'_'+str(i + 1)]
                j += 1
            i += 1

        #check if some attribute is not on the fds and add a table with it
        missing_attrs = []
        for a in old_table.get_attributes:
            if a.get_name not in checked_attributes:
                missing_attrs.append(a)
        if len(missing_attrs) > 0:
            generated_tables[old_table.get_name+'_'+str(i + 1)] = {'attr': missing_attrs, 'fds': []}
            i += 1

        for t in generated_tables:
            new_table_obj = Table(t)
            new_table_obj.set_fds(generated_tables[t]['fds'])
            new_table_obj.set_attributes(generated_tables[t]['attr'])
            new_tables.append(new_table_obj)

        #check if the candidate keys are not on the fds and add a table for one of them
        cks = self.nf.get_candidate_keys()
        has_candidate_key = False
        for t in new_tables:
            t_attr = [a.get_name for a in t.get_attributes]
            for ck in cks:
                ck_attr = [a.get_name for a in ck]
                if set(ck_attr) < set(t_attr):
                    has_candidate_key = True

        if not has_candidate_key:
            new_table_obj = Table(old_table.get_name+'_'+str(i+1))
            new_table_obj.set_attributes(cks[0])
            new_tables.append(new_table_obj)

        self.new_tables = new_tables


#from dbnormalizer.core.importdata.XMLImport import XMLImport
#from dbnormalizer.core.normalizer.NF import NF

#test = XMLImport('/Users/mairamachadoladeira/PycharmProjects/adb_project/examples/slide2_p14.xml', True)
#test.init_objects()
#schema = test.get_schema()
#table = schema.get_table_by_name('TEST')
#nf = NF(table)
#normalization = Normalizer(nf)
#normalization.decomposition()
#print(normalization.get_new_tables())