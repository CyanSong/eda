from device.linear_device import linear_device


class cccs(linear_device):
    def __init__(self, name, pos_node, neg_node, v_src, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)
        self.v_src = v_src

    def make_stamp(self, mat, vec, freq=0):
        index = self.v_src.index
        mat[self.pos_node.num][index] += self.val
        mat[self.neg_node.num][index] -= self.val

    def get_current(self, rst_vec, freq=0):
        ctl_cur = self.v_src.get_current(rst_vec)
        return self.val * ctl_cur
