from device.linear_device import linear_device


class idc(linear_device):
    def __init__(self, name, pos_node, neg_node, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)

    def make_stamp(self, mat, vec):
        assert (self.pos_node.num < len(vec) and self.pos_node.num < len(vec))
        vec[self.pos_node.num][0] -= self.val
        vec[self.neg_node.num][0] += self.val

    def get_dc_current(self):
        return self.val
