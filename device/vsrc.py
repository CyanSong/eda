from cmath import rect

from device.device import *


class vsrc(linear_device):
    def __init__(self, name, pos_node, neg_node, src_type="dc", dc_val=None, ac_mag=0, ac_phase=0, func=None):
        double_port_device.__init__(self, name, pos_node, neg_node, dc_val)
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
        return rst_vec[self.index]

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
