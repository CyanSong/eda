from device.device import *


class ind(linear_device):
    def __init__(self, name, pos_node, neg_node, val):
        double_port_device.__init__(self, name, pos_node, neg_node, val)
        self.index = None

    def put_index(self, index):
        self.index = index

    def del_index(self):
        self.index = None

    def make_stamp(self, mat, vec, freq=0):
        assert (self.index is not None)
        sl = self.val * (complex(0, freq) if freq != 0 else 0)
        mat[self.index][self.index] -= sl
        mat[self.pos_node.num][self.index] += 1
        mat[self.neg_node.num][self.index] -= 1
        mat[self.index][self.neg_node.num] -= 1
        mat[self.index][self.pos_node.num] += 1

    def make_tran_stamp(self, mat, vec, h, rst_last, method='trap'):
        if rst_last is None:
            mat[self.index][self.index] = 1
        else:
            h_L = h / self.val
            v_last = rst_last[self.pos_node.num] - rst_last[self.neg_node.num]
            if method == 'trap':
                i_last = rst_last[self.index]
                mat[self.pos_node.num][self.index] += 1
                mat[self.neg_node.num][self.index] -= 1
                mat[self.index][self.index] -= 1
                mat[self.index][self.pos_node.num] += 2 * h_L
                mat[self.index][self.neg_node.num] -= 2 * h_L
                vec[self.index][0] -= (2 * h_L * v_last + i_last)

    def get_current(self, rst_vec, freq=0):
        return rst_vec[self.index]
