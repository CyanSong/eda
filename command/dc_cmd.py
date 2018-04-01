import functools
import logging
from multiprocessing import Pool

from basic import *
from command.task import task


class dc_task(task):
    def __init__(self, src1, start1, stop1, incr1, src2=None, start2=None, stop2=None, incr2=None):
        self.src1, self.start1, self.stop1, self.incr1 = src1, start1, stop1, incr1
        if src2 is not None:
            self.src2, self.start2, self.stop2, self.incr2 = src2, start2, stop2, incr2

    def generate_seq(self):
        return list(np.arange(self.start1, self.stop1, self.incr1))


def get_dc_task(cmd_tree):
    if len(cmd_tree.children) == 1:
        src = cmd_tree.children[0].children[0]
        vsrc = src.children[0].data + src.children[1].value
        dsrc = [parse_value(i, float) for i in cmd_tree.children[0].children[1:]]
        return dc_task(vsrc, dsrc[0], dsrc[1], dsrc[2])
    else:
        pass


def dc_handler(net, t):
    ground_node = net.node_dict["0"].num
    basic_len = len(net.node_dict)
    elements = net.elements
    arg = t.generate_seq()
    vname = t.src1
    solver = functools.partial(dc_solver, ground_node, basic_len, elements, vname)

    if len(arg) * len(elements) ** 2 > 125000:
        with Pool(4) as pool:
            rst = pool.map(solver, arg)
    else:
        rst = [solver(i) for i in arg]
    logging.debug(rst)
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
