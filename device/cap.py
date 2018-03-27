from device.linear_device import linear_device
from basic import *


def get_cap(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "c" + element_tree.children[0].value
    val = parse_value(element_tree.children[3])
    return cap(name, nodes[0], nodes[1], val)


class cap(linear_device):
    def __init__(self, name, pos_node, neg_node, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)

    def make_stamp(self, mat, vec, freq):
        sc = self.val * complex(0, freq)
        mat[self.pos_node.num][self.pos_node.num] += sc
        mat[self.pos_node.num][self.neg_node.num] -= sc
        mat[self.neg_node.num][self.pos_node.num] -= sc
        mat[self.neg_node.num][self.neg_node.num] += sc
