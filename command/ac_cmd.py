import functools
from multiprocessing import Pool

from basic import *
from command.task import task


class ac_task(task):
    def __init__(self, number, start, stop, mode='dec'):
        self.mode = mode
        self.number = number
        self.start = start
        self.stop = stop

    # TODO:need to modify to sopport more mode
    def generate_seq(self):
        return [self.start + (self.stop - self.start) / self.number * i for i in range(self.number)]


def get_ac_task(cmd):
    if len(cmd.children) == 3:
        return ac_task(parse_value(cmd.children[0], int), parse_value(cmd.children[1], float),
                       parse_value(cmd.children[2], float))
    else:
        return ac_task(parse_value(cmd.children[1], int), parse_value(cmd.children[2], float),
                       parse_value(cmd.children[3], float), cmd.children[0])


def ac_handler(net, t):
    ground_node = net.node_dict["0"].num
    basic_len = len(net.node_dict)
    elements = net.elements
    arg = t.generate_seq()
    solver = functools.partial(ac_solver, ground_node, basic_len, elements)

    if len(arg) * len(elements) ** 2 > 125000:
        with Pool(4) as pool:
            rst = pool.map(solver, arg)
    else:
        rst = [solver(i) for i in arg]
    return rst


def ac_solver(ground_node, basic_len, elements_dict, freq):
    a, b = generate_linear_equation(basic_len, elements_dict, 'ac')
    for i in elements_dict.values():
        i.make_stamp(a, b, freq)
    index = list(range(len(a)))
    index.remove(ground_node)
    a, b = a[np.ix_(index, index)], b[np.ix_(index, [0])]
    rst = list(np.linalg.solve(a, b))
    rst.insert(ground_node, [0])
    return np.array(rst)[:, 0]
