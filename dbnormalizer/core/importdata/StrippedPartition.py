__author__ = 'Iva'

class StrippedPartition:

    def __init__(self, column, result_set):
        self.elements = []
        self.no_of_sets = 0
        self.no_of_elem = 0
        self.result_set = result_set
        self.dict_part = {}

        id_row = 1
        for data in result_set:
            row = str(data[column])
            #row =1
            if row is None:
                row = "NULL"
            #if already in dictionary
            if row in self.dict_part:
                value_list = self.dict_part.get(row)
                value_list.append(id_row)
                self.dict_part[row] = value_list
            else:
                value_list = []
                value_list.append(id_row)
                self.dict_part[row] = value_list
            id_row += 1
        for val_l in self.dict_part.values():
            if len(val_l) > 1:
                self.elements = val_l
                self.no_of_elem += len(val_l)
                self.no_of_sets += 1
        self.error = self.no_of_elem - self.no_of_sets
        #empty dictionary for memory
        self.dict_part = {}



