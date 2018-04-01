from cmath import rect

from basic import *
from device.linear_device import linear_device


def get_vsrc(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "v" + element_tree.children[0].value
    spec = element_tree.children[3]

    if spec.data == 'vdc':
        src_type = 'dc'
        dc_val = parse_value(spec.children[-1], float)
        return vsrc(name, nodes[0], nodes[1], src_type=src_type, dc_val=dc_val)
    else:
        src_type = 'ac'
        ac_mag = parse_value(spec.children[0]) if len(spec.children) > 0 else 0
        ac_phase = parse_value(spec.children[1]) if len(spec.children) > 1 else 0
        return vsrc(name, nodes[0], nodes[1], src_type, ac_mag=ac_mag, ac_phase=ac_phase)


class vsrc(linear_device):
    def __init__(self, name, pos_node, neg_node, src_type="dc", dc_val=None, ac_mag=0, ac_phase=0, func=None):
        linear_device.__init__(self, name, pos_node, neg_node, dc_val)
        self.src_type = src_type
        if src_type == "ac":
            self.ac_val = rect(ac_mag, ac_phase)
        else:
            self.ac_val = None
        self.func = func
        self.index = None

    def put_index(self, index):
        self.index = index

    def del_index(self):
        self.index = None

    def get_current(self, rst_vec, freq=0):
        return rst_vec[self.index][0]

    def make_stamp(self, mat, vec, freq=0, val=None):
        assert (self.index is not None)
        mat[self.index][self.pos_node.num] += 1
        mat[self.index][self.neg_node.num] -= 1
        mat[self.pos_node.num][self.index] += 1
        mat[self.neg_node.num][self.index] -= 1
        if freq == 0:
            assert (self.val is not None)
            val = self.val if val is None else val
            vec[self.index] = val + vec[self.index]
        else:
            assert (self.ac_val is not None)
            vec[self.index] = self.ac_val + vec[self.index]
