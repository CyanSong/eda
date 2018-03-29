from device.linear_device import linear_device
from basic import *


def get_ccvs(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "h" + element_tree.children[0].value
    val = parse_value(element_tree.children[4])
    vsrc_name = element_tree.children[3]
    return ccvs(name, nodes[0], nodes[1], vsrc_name, val)


class ccvs(linear_device):
    def __init__(self, name, pos_node, neg_node, v_src, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)
        self.v_src = v_src
        self.index = None
        self.current = None

    def put_index(self, index):
        self.index = index

    def get_current(self, rst_vec, freq=0):
        return rst_vec[self.index][0]

    def make_stamp(self, mat, vec=None, freq=None):
        index = self.v_src.index
        assert (self.index is not None and index is not None)
        mat[self.index][index] -= self.val
        mat[self.index][self.pos_node.num] += 1
        mat[self.index][self.neg_node.num] -= 1
        mat[self.pos_node.num][self.index] += 1
        mat[self.neg_node.num][self.index] -= 1
