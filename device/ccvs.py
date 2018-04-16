from device.device import *


class ccvs(linear_device):
    def __init__(self, name, pos_node, neg_node, v_src, val):
        double_port_device.__init__(self, name, pos_node, neg_node, val)
        self.v_src = v_src
        self.index = None

    def put_index(self, index):
        self.index = index

    def del_index(self):
        self.index = None

    def get_current(self, rst_vec, freq=0):
        return rst_vec[self.index]

    def make_stamp(self, type, mat, vec, **kwargs):
        index = self.v_src.index
        assert (self.index is not None and index is not None)
        mat[self.index][index] -= self.val
        mat[self.index][self.pos_node.num] += 1
        mat[self.index][self.neg_node.num] -= 1
        mat[self.pos_node.num][self.index] += 1
        mat[self.neg_node.num][self.index] -= 1
