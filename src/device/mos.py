from device.device import *
from src import error

default_l = 1
default_w = 1


class mos(device):
    def __init__(self, name, d_node, g_node, s_node, b_node, model_type, l=default_l, w=default_w):
        device.__init__(self, name)
        self.d_node = d_node
        self.g_node = g_node
        self.s_node = s_node
        self.b_node = b_node
        self.length = l
        self.width = w
        self.model_type = model_type
        if self.model_type == 'nmos':
            self.vt = 0.43
            self.k = 115 * (10 ** -6)
        else:
            self.vt = -0.4
            self.k = -30 * (10 ** -6)

    def make_stamp(self, type, mat, vec, **kwargs):
        try:
            last_itr = kwargs['last_itr']
        except KeyError:
            raise error.internal_error("Loss of argument!")

        if last_itr is None:
            pass
        else:
            vds = self.d_node.get_voltage(last_itr) - self.s_node.get_voltage(last_itr)
            vgs = self.g_node.get_voltage(last_itr) - self.s_node.get_voltage(last_itr)
            p_n = 1 if self.model_type == 'nmos' else -1
            if p_n * vgs < p_n * self.vt:
                pass
            else:
                k = self.width / self.length * self.k
                if p_n * vds > p_n * vgs - p_n * self.vt:
                    gds = 0
                    gm = k * (vgs - self.vt)
                    ids = 1 / 2 * k * (vgs - self.vt) ** 2
                else:
                    ids = k * ((vgs - self.vt) * vds - 1 / 2 * (vds ** 2))
                    gm = k * vds
                    gds = k * (vgs - self.vt - vds)
                ids = ids - gm * vgs - gds * vds
                vec[self.d_node.num][0] -= ids
                vec[self.s_node.num][0] += ids
                mat[self.d_node.num][self.d_node.num] += gds
                mat[self.d_node.num][self.s_node.num] -= (gds + gm)
                mat[self.d_node.num][self.g_node.num] += gm
                mat[self.s_node.num][self.d_node.num] -= gds
                mat[self.s_node.num][self.s_node.num] += (gds + gm)
                mat[self.s_node.num][self.g_node.num] -= gm
