from device.linear_device import linear_device
from basic import *
from cmath import rect


def get_vsrc(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "v" + element_tree.children[0].value
    spec = element_tree.children[3]
    src_type = 'dc'
    print(spec)
    if spec.data == 'dc':
        dc_val = spec.children[-1]
        return vsrc(name, nodes[0], nodes[1], src_type, dc_val)
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
        self.current = None

    def put_index(self, index):
        self.index = index

    def put_dc_current(self, current):
        self.current = current

    def get_dc_current(self):
        assert (self.current is not None)
        return self.current

    def make_stamp(self, mat, vec, freq=None):
        assert (self.index is not None)
        mat[self.index][self.pos_node.num] += 1
        mat[self.index][self.neg_node.num] -= 1
        mat[self.pos_node.num][self.index] += 1
        mat[self.neg_node.num][self.index] -= 1
        if freq == 0:
            vec[self.index] += self.val
        else:
            assert (self.ac_val is not None)
            vec[self.index] = self.ac_val+vec[self.index]
