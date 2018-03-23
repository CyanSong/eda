from device.linear_device import linear_device


class vccs(linear_device):
    def __init__(self, name, pos_node, neg_node, ctl_pos_node, ctl_neg_node, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)
        self.ctl_neg_node = ctl_neg_node
        self.ctl_pos_node = ctl_pos_node

    def make_stamp(self, mat, vec):
        assert (max(self.pos_node.num, self.neg_node.num, self.ctl_neg_node.num, self.ctl_pos_node.num) < len(mat))
        mat[self.pos_node.num][self.ctl_pos_node.num] += self.val
        mat[self.pos_node.num][self.ctl_neg_node.num] -= self.val
        mat[self.neg_node.num][self.ctl_pos_node.num] -= self.val
        mat[self.neg_node.num][self.ctl_neg_node.num] += self.val

    def get_dc_current(self):
        ctl_vol_diff = self.ctl_pos_node.get_voltage() - self.ctl_neg_node.get_voltage()
        return ctl_vol_diff * self.val
