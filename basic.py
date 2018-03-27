def parse_value(value_tree):
    simple_unit_dict = {"k": 1000, "p": 10 ** -12, "n": 10 ** -9, "u": 10 ** -6, "m": 10 ** 6, "f": 10 ** -15}
    # only support "k" | "p" | "n" | "u" | "m" | "f" now
    if hasattr(value_tree.children[0], "unit"):
        if value_tree.children[0].unit in simple_unit_dict.keys():
            return float(value_tree.children[0].value) * simple_unit_dict[value_tree.children[0].unit]
        else:
            # ToDo support "meg" | "g" | "t" | "db"
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
        self.voltage = None

    def get_voltage(self):
        assert (self.voltage is not None)
        return self.voltage

    def put_voltage(self, val):
        self.voltage = val
