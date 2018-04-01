from basic import *
from command.task import task


class tran_task(task):
    def __init__(self, step, stop, start=0, max=-1):
        self.step, self.stop, self.start = step, stop, start
        h = min(self.step, (self.stop - self.start) / 50)
        self.h = min(h, max) if max != -1 else h

    def generate_seq(self):
        return list(np.arange(0, self.stop, self.h))

    def cut_seq(self, seq):
        return seq[int((self.start - 0) / self.h):]


def get_tran_task(cmd_tree):
    seq = [parse_value(i, float) for i in cmd_tree.children]
    return tran_task(*seq)


def tran_handler(net, t):
    ground_node = net.node_dict["0"].num
    basic_len = len(net.node_dict)
    elements = net.elements
    seq = t.generate_seq()
    h = t.h
    rst = [None]
    for _ in seq:
        rst.append(tran_solver(ground_node, basic_len, elements, h, rst[-1]))
    rst = t.cut_seq(rst[1:])
    return rst


def tran_solver(ground_node, basic_len, elements_dict, h, rst_last):
    a, b = generate_linear_equation(basic_len, elements_dict, 'tran')
    for i in elements_dict.keys():
        if hasattr(elements_dict[i], 'make_tran_stamp'):
            elements_dict[i].make_tran_stamp(a, b, h, rst_last)
        else:
            elements_dict[i].make_stamp(a, b)
    index = list(range(len(a)))
    index.remove(ground_node)
    a, b = a[np.ix_(index, index)], b[np.ix_(index, [0])]
    rst = list(np.linalg.solve(a, b))
    rst.insert(ground_node, [0])
    for i in elements_dict.values():
        if hasattr(i, "index"):
            i.del_index()
    return np.array(rst)[:, 0]
