from device.device import *


class isrc(linear_device):
    def __init__(self, name, pos_node, neg_node, val):
        double_port_device.__init__(self, name, pos_node, neg_node, val)

    def make_stamp(self, type, mat, vec, **kwargs):
        val = kwargs['val'] if 'val' in kwargs.keys() else self.val
        assert (self.pos_node.num < len(vec) and self.pos_node.num < len(vec))
        vec[self.pos_node.num][0] -= val
        vec[self.neg_node.num][0] += val

    def get_current(self, rst_vec):
        return self.val
