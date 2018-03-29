from device.linear_device import linear_device
from basic import *


def get_cccs(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "f" + element_tree.children[0].value
    vsrc_name = element_tree.children[3]
    val = parse_value(element_tree.children[4])
    return cccs(name, nodes[0], nodes[1], vsrc_name, val)


class cccs(linear_device):
    def __init__(self, name, pos_node, neg_node, v_src, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)
        self.v_src = v_src

    def make_stamp(self, mat, vec=None, freq=None):
        index = self.v_src.index
        mat[self.pos_node.num][index] += self.val
        mat[self.neg_node.num][index] -= self.val

    def get_current(self,rst_vec,freq=0):
        ctl_cur = self.v_src.get_current(rst_vec)
        return self.val * ctl_cur

