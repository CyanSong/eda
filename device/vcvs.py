from device.linear_device import linear_device


class vcvs(linear_device):
    def __init__(self, name, pos_node, neg_node, ctl_pos_node, ctl_neg_node, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)
        self.ctl_neg_node = ctl_neg_node
        self.ctl_pos_node = ctl_pos_node
        self.index = None
        self.current = None

    def put_index(self, index):
        self.index = index

    def del_index(self):
        self.index = None

    def get_current(self, rst_vec, freq=0):
        return rst_vec[self.index]

    def make_stamp(self, mat, vec, freq=0):
        assert (self.index is not None)
        mat[self.index][self.pos_node.num] += 1
        mat[self.index][self.neg_node.num] -= 1
        mat[self.index][self.ctl_pos_node.num] -= self.val
        mat[self.index][self.ctl_neg_node.num] += self.val
        mat[self.pos_node.num][self.index] += 1
        mat[self.neg_node.num][self.index] -= 1
