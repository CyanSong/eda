from .device import linear_device,double_port_device

class vccs(linear_device):
    def __init__(self, name, pos_node, neg_node, ctl_pos_node, ctl_neg_node, val):
        double_port_device.__init__(self, name, pos_node, neg_node, val)
        self.ctl_neg_node = ctl_neg_node
        self.ctl_pos_node = ctl_pos_node

    def make_stamp(self, type, mat, vec, **kwargs):
        assert (max(self.pos_node.num, self.neg_node.num, self.ctl_neg_node.num, self.ctl_pos_node.num) < len(mat))
        mat[self.pos_node.num][self.ctl_pos_node.num] += self.val
        mat[self.pos_node.num][self.ctl_neg_node.num] -= self.val
        mat[self.neg_node.num][self.ctl_pos_node.num] -= self.val
        mat[self.neg_node.num][self.ctl_neg_node.num] += self.val

    def get_current(self, rst_vec, freq=0):
        ctl_vol_diff = self.ctl_pos_node.get_voltage(rst_vec) - self.ctl_neg_node.get_voltage(rst_vec)
        return ctl_vol_diff * self.val
