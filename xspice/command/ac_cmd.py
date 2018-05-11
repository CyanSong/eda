import functools
from multiprocessing import Pool

import numpy as np

from .basic_solver import basic_solver
from .handler import handler


class ac_handler(handler):
    def __init__(self, net, t):
        handler.__init__(self, net, t)
        self.scale_limit = 125000

    def handle(self):
        print("Begin the ac simulation.")
        ground_node, basic_len, elements, seq = handler.handle(self)
        solver = functools.partial(ac_solver, ground_node, basic_len, elements, self.net.linear)

        if len(seq) * len(elements) ** 2 > self.scale_limit:
            with Pool(4) as pool:
                rst = np.array(pool.map(solver, seq))
        else:
            rst = np.array([solver(i) for i in seq])
        print("Finish the ac simulation.")
        return seq, rst

    def get_axis_mode(self):
        return self.task.mode


def ac_solver(ground_node, basic_len, elements_dict, linear, freq):
    return basic_solver(ground_node, basic_len, elements_dict, 'ac', linear, freq=freq)
