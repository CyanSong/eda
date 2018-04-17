import functools
from multiprocessing import Pool

from basic import *
from command.basic_solver import basic_solver
from command.handler import handler
from error import *


# TODO implement homotopy
class dc_handler(handler):
    def __init__(self, net, t):
        self.error_bound = 10 ** -6
        self.max_iter = 1000
        handler.__init__(self, net, t)

    def handle(self):
        print("Begin the dc simulation.")
        ground_node, basic_len, elements, seq = handler.handle(self)
        vname = self.task.src1
        if vname not in self.net.elements.keys():
            raise net_definition_error("The element: {} is not defined".format(vname))
        solver = functools.partial(dc_solver, ground_node, basic_len, elements, self.net.linear, self.error_bound,
                                   self.max_iter, vname)
        if len(seq) * len(elements) ** 2 > 125000:
            with Pool(4) as pool:
                rst = np.array(pool.map(solver, seq))
        else:
            rst = np.array([solver(i) for i in seq])
        print("Finish the dc simulation.")
        return seq, rst


def dc_solver(ground_node, basic_len, elements_dict, linear, error_bound, max_iter, vname=None, val=None):
    new_rst = basic_solver(ground_node, basic_len, elements_dict, 'dc', linear, vname=vname, val=val, last_itr=None)
    if not linear:
        old_rst = np.ones(shape=new_rst.shape) * np.Inf
        iter_num = 0
        while np.linalg.norm(new_rst - old_rst, np.Inf) > error_bound and iter_num < max_iter:
            # print("iter {} result vector:{}".format(iter_num + 1, new_rst))
            old_rst = new_rst
            new_rst = basic_solver(ground_node, basic_len, elements_dict, 'dc', linear, last_itr=old_rst,
                                   vname=vname, val=val)
            iter_num += 1
        if iter_num == max_iter:
            print("Warning: iteration reach maximum number and the circuit may not converge!")
    return new_rst
