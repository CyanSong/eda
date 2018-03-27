from device.linear_device import linear_device
from basic import *


def get_vccs(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:5]], node_dict)
    name = "g" + element_tree.children[0].value
    val = parse_value(element_tree.children[5])
    return vccs(name, nodes[0], nodes[1], nodes[2], nodes[3], val)


class vccs(linear_device):
    def __init__(self, name, pos_node, neg_node, ctl_pos_node, ctl_neg_node, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)
        self.ctl_neg_node = ctl_neg_node
        self.ctl_pos_node = ctl_pos_node

    def make_stamp(self, mat, vec=None, freq=None):
        assert (max(self.pos_node.num, self.neg_node.num, self.ctl_neg_node.num, self.ctl_pos_node.num) < len(mat))
        mat[self.pos_node.num][self.ctl_pos_node.num] += self.val
        mat[self.pos_node.num][self.ctl_neg_node.num] -= self.val
        mat[self.neg_node.num][self.ctl_pos_node.num] -= self.val
        mat[self.neg_node.num][self.ctl_neg_node.num] += self.val

    def get_dc_current(self):
        ctl_vol_diff = self.ctl_pos_node.get_voltage() - self.ctl_neg_node.get_voltage()
        return ctl_vol_diff * self.val
