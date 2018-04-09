import math

from device.device import *


class diode(double_port_device):
    def __init__(self, name, pos_node, neg_node, val=1, alpha=40, ic=0):
        super().__init__(name, pos_node, neg_node, val)
        self.ic = ic
        self.alpha = alpha

    def make_stamp(self, mat, vec, freq=0,last_rst=None):
        if last_rst is None:
            v_d = self.ic
            i_d = self.val * (math.exp(self.alpha * v_d) - 1)
        else:
            v_d = self.pos_node.get_voltage(last_rst) - self.neg_node.get_voltage(last_rst)
            i_d = self.get_current(last_rst)
        g_0 = self.alpha * math.exp(self.alpha * v_d) * self.val
        i_0 = i_d - g_0 * v_d
        vec[self.pos_node.num][0] -= i_0
        vec[self.neg_node.num][0] += i_0
        mat[self.pos_node.num][self.pos_node.num] += g_0
        mat[self.pos_node.num][self.neg_node.num] -= g_0
        mat[self.neg_node.num][self.pos_node.num] -= g_0
        mat[self.neg_node.num][self.neg_node.num] += g_0

    def get_current(self, rst_vec):
        v_d = self.pos_node.get_voltage(rst_vec) - self.neg_node.get_voltage(rst_vec)
        return self.val * (math.exp(self.alpha * v_d) - 1)
