__author__ = 'Maira'


def get_attributes_list(attributes):
    attributes_list = []
    for attr in attributes:
        attributes_list.append(attr.get_name)
    return attributes_list


def get_fds_list(fds):
    functional_dependencies = []
    for fd in fds:
        lhs_attributes = []
        rhs_attributes = []
        lhs = fd.get_lhs
        rhs = fd.get_rhs
        for attr in lhs:
            lhs_attributes.append(attr.get_name)
        for attr in rhs:
            rhs_attributes.append(attr.get_name)
        fd = {
            'lhs': lhs_attributes,
            'rhs': rhs_attributes
        }
        functional_dependencies.append(fd)
    return functional_dependencies