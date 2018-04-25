import math

import numpy as np


def parse_value(value_tree, t=float):
    simple_unit_dict = {"k": 1000, "p": 10 ** -12, "n": 10 ** -9, "u": 10 ** -6, "m": 10 ** -3, "f": 10 ** -15,
                        "meg": 10 ** 3, 'g': 10 ** 6, 't': 10 ** 9}

    if len(value_tree.children) > 1 and t == float:
        if value_tree.children[1].value in simple_unit_dict.keys():
            return t(value_tree.children[0].value) * simple_unit_dict[value_tree.children[1].value]
        else:
            return 20 * math.log(t(value_tree.children[0].value), 10)
    else:
        return t(value_tree.children[0].value)


def remap_node(node_name_list, node_dict):
    res = []
    for node_name in node_name_list:
        if node_name not in node_dict:
            t = node(node_name, len(node_dict))
            node_dict[node_name] = t
        res.append(node_dict[node_name])
    return res


class node():
    def __init__(self, name, number):
        self.name = name
        self.num = number

    def get_voltage(self, rst_vec):
        return rst_vec[self.num]


def generate_linear_equation(basic_len, elements, mode):
    index = 0
    v_node_num = basic_len
    for i in elements.values():
        if hasattr(i, "index") or (hasattr(i, 'tran_index') and mode == 'tran'):
            i.put_index(index + v_node_num)
            index += 1
    dtype = np.complex128 if mode == "ac" else np.float64
    return np.zeros((v_node_num + index, v_node_num + index), dtype=dtype), np.zeros((v_node_num + index, 1),
                                                                                     dtype=dtype)


class src_fun():
    pass


class sin(src_fun):

    def __init__(self, v0, va, freq, td=0, theta=1):
        self.v0 = v0
        self.va = va
        self.cycle = 1 / freq
        self.td = td
        self.theta = theta

    def fun(self, x):
        main = self.va * np.sin((x - self.td) / self.cycle * 2 * np.pi) if x > self.td else 0
        factor = self.theta ** (x / self.cycle) if self.theta != 1 else 1
        return main * factor + self.v0


class pulse(src_fun):

    def __init__(self, v1, v2, td, tr, tf, pw, per):
        self.v1 = v1
        self.v2 = v2
        self.cycle = per
        self.pw = pw
        self.td = td
        self.tr = tr
        self.tf = tf
        self.phase1 = self.cycle - self.pw - self.tr - self.tf
        self.phase2 = self.cycle - self.pw - self.tf
        self.phase3 = self.cycle - self.tf

    def fun(self, x):
        if x < self.td:
            return 0

        x = (x - self.td) % self.cycle

        if x <= self.phase1:
            return self.v1
        elif self.phase2 <= x <= self.phase3:
            return self.v2
        elif self.phase1 < x < self.phase2:
            return (x - self.phase1) / self.tr * (self.v2 - self.v1) + self.v1
        else:
            return self.v1 + (self.cycle - x) / self.tf * (self.v2 - self.v1)
