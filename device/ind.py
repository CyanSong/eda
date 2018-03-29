from device.linear_device import linear_device
from basic import *


def get_ind(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "l" + element_tree.children[0].value
    val = parse_value(element_tree.children[3])
    return ind(name, nodes[0], nodes[1], val)


class ind(linear_device):
    def __init__(self, name, pos_node, neg_node, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)
        self.index = None

    def put_index(self, index):
        self.index = index

    def make_stamp(self, mat, vec, freq):
        assert (self.index is not None)
        sl = self.val * (complex(0, freq) if freq!=0 else 0)
        mat[self.index][self.index] -= sl
        mat[self.pos_node.num][self.index] += 1
        mat[self.neg_node.num][self.index] -= 1
        mat[self.index][self.neg_node.num] -= 1
        mat[self.index][self.pos_node.num] += 1

    def get_current(self,rst_vec,freq=0):
        return rst_vec[self.index][0]
