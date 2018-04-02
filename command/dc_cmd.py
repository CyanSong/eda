import functools
from multiprocessing import Pool
from basic import *
from command.task import *
from command.handler import handler


class dc_handler(handler):
    def __init__(self, net, t):
        handler.__init__(self, net, t)

    def handle(self):
        ground_node, basic_len, elements, seq = handler.handle(self)
        vname = self.task.src1
        solver = functools.partial(dc_solver, ground_node, basic_len, elements, vname)
        if len(seq) * len(elements) ** 2 > 125000:
            with Pool(4) as pool:
                rst = pool.map(solver, seq)
        else:
            rst = [solver(i) for i in seq]
        return rst


def dc_solver(ground_node, basic_len, elements_dict, vname=None, val=None):
    a, b = generate_linear_equation(basic_len, elements_dict, 'dc')
    for i in elements_dict.keys():
        if i != vname:
            elements_dict[i].make_stamp(a, b, 0)
        else:
            elements_dict[i].make_stamp(a, b, 0, val)
    index = list(range(len(a)))
    index.remove(ground_node)
    a, b = a[np.ix_(index, index)], b[np.ix_(index, [0])]
    rst = list(np.linalg.solve(a, b))
    rst.insert(ground_node, [0])
    return np.array(rst)[:, 0]
