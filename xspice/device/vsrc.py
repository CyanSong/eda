from cmath import rect

from .device import linear_device, double_port_device
from ..error import internal_error


class vsrc(linear_device):
    def __init__(self, name, pos_node, neg_node, src_type="dc", dc_val=0, **kwargs):
        double_port_device.__init__(self, name, pos_node, neg_node, dc_val)
        self.src_type = src_type
        try:
            if src_type == "ac":
                self.ac_val = rect(kwargs['ac_mag'], kwargs['ac_phase'])
            elif src_type == 'dc':
                self.ac_val = None
            else:
                self.func = kwargs['fun']
        except KeyError:
            raise internal_error("Loss of argument!")

        self.index = None

    def put_index(self, index):
        self.index = index

    def del_index(self):
        self.index = None

    def get_current(self, rst_vec, freq=0):
        return rst_vec[self.index]

    def make_stamp(self, type, mat, vec, **kwargs):
        assert (self.index is not None)
        mat[self.index][self.pos_node.num] += 1
        mat[self.index][self.neg_node.num] -= 1
        mat[self.pos_node.num][self.index] += 1
        mat[self.neg_node.num][self.index] -= 1

        if type == 'dc':
            val = self.val if 'val' not in kwargs.keys() else kwargs['val']
        elif type == 'tran':
            if self.src_type == 'fun':
                try:
                    t = kwargs['t']
                except KeyError:
                    raise internal_error("Loss of argument!")
                val = self.func.fun(t)
            else:
                val = self.val
        else:
            val = self.ac_val

        vec[self.index][0] += val
