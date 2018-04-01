from basic import *
from device.linear_device import linear_device


def get_vcvs(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:5]], node_dict)
    name = "e" + element_tree.children[0].value
    val = parse_value(element_tree.children[5])
    return vcvs(name, nodes[0], nodes[1], nodes[2], nodes[3], val)


class vcvs(linear_device):
    def __init__(self, name, pos_node, neg_node, ctl_pos_node, ctl_neg_node, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)
        self.ctl_neg_node = ctl_neg_node
        self.ctl_pos_node = ctl_pos_node
        self.index = None
        self.current = None

    def put_index(self, index):
        self.index = index

    def del_index(self):
        self.index=None

    def get_current(self, rst_vec, freq=0):
        return rst_vec[self.index][0]

    def make_stamp(self, mat, vec, freq=0):
        assert (self.index is not None)
        mat[self.index][self.pos_node.num] += 1
        mat[self.index][self.neg_node.num] -= 1
        mat[self.index][self.ctl_pos_node.num] -= self.val
        mat[self.index][self.ctl_neg_node.num] += self.val
        mat[self.pos_node.num][self.index] += 1
        mat[self.neg_node.num][self.index] -= 1
