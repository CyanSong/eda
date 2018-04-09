from device.device import *


class isrc(linear_device):
    def __init__(self, name, pos_node, neg_node, val):
        double_port_device.__init__(self, name, pos_node, neg_node, val)

    def make_stamp(self, mat, vec, freq=0, val=None):
        assert (self.pos_node.num < len(vec) and self.pos_node.num < len(vec))
        val = self.val if val is None else val
        vec[self.pos_node.num][0] -= val
        vec[self.neg_node.num][0] += val

    def get_current(self, rst_vec):
        return self.val
