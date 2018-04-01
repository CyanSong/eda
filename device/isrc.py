from basic import *
from device.linear_device import linear_device


def get_isrc(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "i" + element_tree.children[0].value
    val = parse_value(element_tree.children[3])
    return isrc(name, nodes[0], nodes[1], val)


class isrc(linear_device):
    def __init__(self, name, pos_node, neg_node, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)

    def make_stamp(self, mat, vec, freq=0, val=None):
        assert (self.pos_node.num < len(vec) and self.pos_node.num < len(vec))
        val = self.val if val is None else val
        vec[self.pos_node.num][0] -= val
        vec[self.neg_node.num][0] += val

    def get_current(self, rst_vec):
        return self.val
