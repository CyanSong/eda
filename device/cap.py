from basic import *
from device.linear_device import linear_device


def get_cap(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "c" + element_tree.children[0].value
    val = parse_value(element_tree.children[3])
    return cap(name, nodes[0], nodes[1], val)


class cap(linear_device):
    def __init__(self, name, pos_node, neg_node, val):
        linear_device.__init__(self, name, pos_node, neg_node, val)
        self.tran_index = None

    def make_stamp(self, mat, vec, freq):
        sc = self.val * (complex(0, freq) if freq != 0 else 0)
        mat[self.pos_node.num][self.pos_node.num] += sc
        mat[self.pos_node.num][self.neg_node.num] -= sc
        mat[self.neg_node.num][self.pos_node.num] -= sc
        mat[self.neg_node.num][self.neg_node.num] += sc

    def put_index(self, index):
        self.tran_index = index

    def del_index(self):
        self.tran_index = None

    def get_current(self, rst_vec, freq=0):
        return (self.pos_node.get_voltage(rst_vec) - self.neg_node.get_voltage(rst_vec)) * self.val * complex(0, freq)

    def make_tran_stamp(self, mat, vec, h, rst_last, method='trap'):
        if rst_last is None:
            mat[self.pos_node.num][self.tran_index] += 1
            mat[self.neg_node.num][self.tran_index] -= 1
            mat[self.tran_index][self.pos_node.num] = 1
            mat[self.tran_index][self.neg_node.num] = 1
        else:
            c_h = self.val / h
            v_last = rst_last[self.pos_node.num] - rst_last[self.neg_node.num]
            if method == 'trap':
                mat[self.pos_node.num][self.tran_index] += 1
                mat[self.neg_node.num][self.tran_index] -= 1
                i_last = rst_last[self.tran_index]
                mat[self.tran_index][self.tran_index] -= 1
                mat[self.tran_index][self.pos_node.num] += c_h * 2
                mat[self.tran_index][self.neg_node.num] -= c_h * 2
                vec[self.tran_index][0] += (i_last + v_last * c_h * 2)
