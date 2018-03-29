import numpy as np
def parse_value(value_tree):
    simple_unit_dict = {"k": 1000, "p": 10 ** -12, "n": 10 ** -9, "u": 10 ** -6, "m": 10 ** -3, "f": 10 ** -15,
                        "meg": 10 ** 3, 'G': 10 ** 6, 'T': 10 ** 9}
    # only support "k" | "p" | "n" | "u" | "m" | "f" now
    if hasattr(value_tree.children[0], "unit"):
        if value_tree.children[0].unit in simple_unit_dict.keys():
            return float(value_tree.children[0].value) * simple_unit_dict[value_tree.children[0].unit]
        else:
            # ToDo support  "db"
            return float(value_tree.children[0].value)
    else:
        return float(value_tree.children[0].value)


def remap_node(node_name_list, node_dict):
    res = []
    for node_name in node_name_list:
        if node_name not in node_dict:
            t = node(node_name, len(node_dict))
            node_dict[node_name] = t
        res.append(node_dict[node_name])
    return res


class node():
    def __init__(self, name, number):
        self.name = name
        self.num = number

    def get_voltage(self, rst_vec):
        return rst_vec[self.num][0]


def generate_linear_equation(net, ac_dc="dc"):
    index = 0
    v_node_num = len(net.nodeDict)
    for i in net.elements.values():
        if hasattr(i, "index"):
            i.put_index(index + v_node_num)
            index += 1
    dtype = np.float64 if ac_dc == "dc" else np.complex128
    return np.zeros((v_node_num + index, v_node_num + index), dtype=dtype), np.zeros((v_node_num + index, 1),
                                                                                     dtype=dtype)
