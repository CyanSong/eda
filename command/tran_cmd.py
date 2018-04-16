from basic import *
from command.basic_solver import basic_solver
from command.handler import handler
from command.task import *


class tran_handler(handler):
    def __init__(self, net, t):
        handler.__init__(self, net, t)
        self.error_bound = 10 ** -6
        self.max_iter = 10000

    def handle(self):
        print("Begin the tran simulation.")
        ground_node, basic_len, elements, seq = handler.handle(self)
        h = self.task.h
        rst = [None]
        for t in seq:
            rst.append(
                tran_solver(ground_node, basic_len, elements, self.net.linear, self.error_bound, self.max_iter, t, h,
                            rst[-1]))
        rst = rst[1:]
        print("Finish the tran simulation.")
        return rst


def tran_solver(ground_node, basic_len, elements_dict, linear, error_bound, max_iter, t, h, rst_last):
    new_rst = basic_solver(ground_node, basic_len, elements_dict, 'tran', linear, t=t, h=h, last_time=rst_last,
                           last_itr=None)
    if not linear:
        old_rst = np.ones(shape=new_rst.shape) * np.Inf
        iter_num = 0

        while np.linalg.norm(new_rst - old_rst, np.Inf) > error_bound or iter_num > max_iter:
            old_rst = new_rst
            new_rst = basic_solver(ground_node, basic_len, elements_dict, 'tran', linear, t=t, h=h, last_time=rst_last,
                                   last_itr=old_rst)
            iter_num += 1
        if iter_num > max_iter:
            print("Warning: iteration reach maximum number and the circuit may not converge!")
    return new_rst
