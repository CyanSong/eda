import functools
from multiprocessing import Pool

from command.basic_solver import basic_solver
from command.handler import handler


class ac_handler(handler):
    def __init__(self, net, t):
        handler.__init__(self, net, t)

    def handle(self):
        print("Begin the ac simulation.")
        ground_node, basic_len, elements, seq = handler.handle(self)
        solver = functools.partial(ac_solver, ground_node, basic_len, elements, self.net.linear)

        if len(seq) * len(elements) ** 2 > 125000:
            with Pool(4) as pool:
                rst = pool.map(solver, seq)
        else:
            rst = [solver(i) for i in seq]
        print("Finish the dc simulation.")
        return rst


def ac_solver(ground_node, basic_len, elements_dict, linear, freq):
    return basic_solver(ground_node, basic_len, elements_dict, 'ac', linear, freq=freq)
