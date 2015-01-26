# from dbnormalizer.core.normalizer.NF import NF
# from dbnormalizer.core.normalizer.NF3 import NF3
#
# __author__ = 'Maira'
#
#
# class BCNF(NF):
#     def __init__(self):
#         super()
#         self.nf3 = NF3()
#         self.candidate_keys = {'pizza'}
#
#     def is_bcnf(self, fds):
#         if not self.nf3.is_nf3(fds):
#             return False
#         for fd in fds:
#             lhs = fd.get_lhs()
#             rhs = fd.get_rhs()
#             for f in lhs:
#                 if f not in self.candidate_keys:
#                     return False
#         return True