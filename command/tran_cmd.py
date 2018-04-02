from basic import *
from command.task import *
from command.handler import handler


class tran_handler(handler):
    def __init__(self, net, t):
        handler.__init__(self, net, t)

    def handle(self):
        ground_node, basic_len, elements, seq = handler.handle(self)
        h = self.task.h
        rst = [None]
        for _ in seq:
            rst.append(tran_solver(ground_node, basic_len, elements, h, rst[-1]))
        rst = rst[1:]
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
    return np.array(rst)[:, 0]
