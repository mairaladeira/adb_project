# from dbnormalizer.core.table.FD import FD
# from dbnormalizer.core.normalizer.NF import NF
# from dbnormalizer.core.normalizer.NF1 import NF1
#
# __author__ = 'Maira'
#
#
# class NF2(NF):
#     def __init__(self):
#         super()
#         self.nf1 = NF1
#         self.is_nf1 = True
#         self.candidate_keys = []
#
#     def is_nf2(self, table):
#         fds0=table.get_fds
#         fds = []
#         for fd in fds0:
#             for right_e in fd.rhs:
#                 fds.append(FD(fd.get_lhs,[right_e]))
#         if not self.is_nf1:
#             return False
#         candidate_keys = self.candidate_keys[table]
#         ck_names=[]
#         for n in candidate_keys:
#             temp=[a.name for a in n]
#             ck_names.append(temp)
#         try:
#             for fd in fds:
#                 lhs = fd.get_lhs()
#                 rhs = fd.get_rhs()
#                 for r in rhs:
#                     if not self.is_prime_attribute(table,r):
#                         if lhs not in candidate_keys:
#                             lhsn=[l.name for l in lhs]
#                             for c in ck_names:
#                                 if set(lhsn)< set(c):
#                                     return False
#             return True
#         except Exception as ex:
#             print('violates_2NF exception')
#             print(ex)
#
#
# test  = NF2()
# from dbnormalizer.core.importdata.DBImport import DBImport
# #from dbnormalizer.core.normalizer import Table
# proba = DBImport(username='postgres', password='postgres', url='localhost:5432', database='adb_test', dbschema='test')
# #proba.print_table_info()
# maped = proba.map_tables()
#
# for t in maped.get_tables():
#     if t.name == 'testing':
#         test.is_nf2(t)
#
#
#
#
#
