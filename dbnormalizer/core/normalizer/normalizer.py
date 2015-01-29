__author__ = 'Mehreeen'
from dbnormalizer.core.table.FD import FD
from dbnormalizer.core.table.Table import Table
from dbnormalizer.core.normalizer.NF import NF
from dbnormalizer.core.table.FKey import FKey

class Normalizer:
    def __init__(self, normal_form):
        self.nf = normal_form
        # fds for the normalization
        self.fds = self.get_fds_union()
        self.new_tables_nf3 = []
        self.new_tables_bcnf = []
        self.nf3_not_bcnf = False

    def get_new_tables_bcnf(self):
        return self.new_tables_bcnf

    def get_new_tables_nf3(self):
        return self.new_tables_nf3

    def get_nf3_is_not_bcnf(self):
        return self.nf3_not_bcnf

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
    def decomposition_3nf(self):
        generated_tables = {}
        generated_tables_aux = []
        new_tables = []
        checked_attributes = set()
        old_table = self.nf.get_table()
        i = 0

        min_cover = self.nf.get_min_cover()

        #Create a new table for each FD after the union operation
        for fd in self.fds:
            lhs = fd.get_lhs
            rhs = fd.get_rhs
            t_attr = lhs + rhs
            t_fd = [fd]
            for f in min_cover:
                t_attr_name = [a.get_name for a in t_attr]
                attrs = f.get_lhs + f.get_rhs
                attrs_name = [a.get_name for a in attrs]
                if set(t_attr_name) != set(attrs_name) and set(attrs_name) < set(t_attr_name):
                    fd_lhs = [a.get_name for a in fd.get_lhs]
                    f_lhs = [a.get_name for a in f.get_lhs]
                    if set(fd_lhs) != set(f_lhs):
                        t_fd += [f]
            generated_tables[old_table.get_name+'_'+str(i + 1)] = {'attr': t_attr, 'fds': t_fd}
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
                if set(attr_1) < set(attr_2) and set(attr_1) != set(attr_2):
                    nm1 = old_table.get_name+'_'+str(j + 1)
                    nm2 = old_table.get_name+'_'+str(i + 1)
                    skip_fd = False
                    for fd1 in generated_tables[nm1]['fds']:
                        lhs1 = [a.get_name for a in fd1.get_lhs]
                        rhs1 = [a.get_name for a in fd1.get_rhs]
                        for fd2 in generated_tables[nm2]['fds']:
                            lhs2 = [a.get_name for a in fd2.get_lhs]
                            rhs2 = [a.get_name for a in fd2.get_rhs]
                            if set(lhs1) == set(lhs2) or set(rhs1) == set(rhs2):
                                skip_fd = True
                    if not skip_fd:
                        generated_tables[nm1]['fds'] += generated_tables[nm2]['fds']
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

        i = 0
        for t in generated_tables:
            new_table_obj = Table(old_table.get_name+'_'+str(i + 1))
            new_table_obj.set_fds(generated_tables[t]['fds'])
            new_table_obj.set_attributes(generated_tables[t]['attr'])
            new_tables.append(new_table_obj)
            i += 1

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

        return new_tables

    def decomposition_bcnf(self, table):
        nf_table = NF(table)
        current_nf = nf_table.determine_nf()
        if current_nf != 'BCNF':
            new_tables = {}
            violating_fds = nf_table.get_violating_fds()
            i = 0
            rhs_violating = []
            created_tables = []
            for fd in violating_fds:
                attrs = fd.get_lhs + fd.get_rhs
                #a_names = [a.get_name for a in attrs]
                new_tables[table.get_name+'_'+str(i+1)] = {'attrs': attrs, 'fds': [fd]}
                rhs_violating += fd.get_rhs
                i += 1
            rhs_violating_names = [a.get_name for a in rhs_violating]
            new_table_attr = []
            for a in table.get_attributes:
                if a.get_name not in rhs_violating_names:
                    new_table_attr.append(a)
            new_tables[table.get_name+'_'+str(i+1)] = {'attrs': new_table_attr, 'fds': []}
            i = 0
            for t in new_tables:
                new_table_obj = Table(table.get_name+'_'+str(i+1))
                new_table_obj.set_attributes(new_tables[t]['attrs'])
                new_table_obj.set_fds(new_tables[t]['fds'])
                created_tables.append(new_table_obj)
                i += 1
            self.nf3_not_bcnf = True
            return created_tables

        else:
            return [table]

    def decomposition(self):
        tables_nf3 = self.decomposition_3nf()
        new_tables = []
        for table in tables_nf3:
            tables_bcnf = self.decomposition_bcnf(table)
            new_tables += tables_bcnf
        #store both decompositions (up to nf3 and up to bcnf)
        self.set_foreign_keys(tables_nf3)
        self.set_foreign_keys(new_tables)
        self.new_tables_nf3 = tables_nf3
        self.new_tables_bcnf = new_tables


    @staticmethod
    def set_foreign_keys(decom_list):
        table_cknames = {}
        for d in decom_list:
            ck_names = []
            normal_form = NF(d)
            ckeys = normal_form.get_candidate_keys()
            for e in ckeys:
                temp = [a.name for a in e]
                ck_names.append(temp)
            table_cknames[d] = ck_names
        for d1 in decom_list:
            for d2 in decom_list:
                if d2 != d1:
                    for ck in table_cknames[d2]:
                        d1_names = [n.name for n in d1.attributes]
                        if set(ck) <= set(d1_names):
                            newkey = True
                            for f in d1.f_keys:
                                if f.referenced_table == d2.name:
                                    newkey = False
                            if newkey == True:
                                d1.f_keys.append(FKey(ck, d2.name, ck))



