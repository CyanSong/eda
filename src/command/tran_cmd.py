from command.basic_solver import basic_solver
from command.handler import handler
from command.task import *
from device.cap import *
from device.ind import *
from src.basic import *

minus = 10 ** -12


class tran_handler(handler):
    def __init__(self, net, t):
        handler.__init__(self, net, t)
        self.error_bound = 10 ** -6
        self.max_iter = 1000
        self.method = 'trap'

    def handle(self):
        print("Begin the tran simulation.")
        ground_node, basic_len, elements, _ = handler.handle(self)
        step, stop, start = self.task.h, self.task.stop, self.task.start
        rst = [None]
        t_list = [start]
        h = step
        while True:
            rst.append(
                tran_solver(ground_node, basic_len, elements, self.net.linear, self.error_bound, self.max_iter,
                            t_list[-1], h,
                            rst[-1]))
            h = auto_get_h(self.method, elements, t_list, rst[1:], step, self.error_bound)
            if t_list[-1] + h < stop:
                t_list.append(t_list[-1] + h)
            else:
                break
        rst = rst[1:]
        print("Finish the tran simulation.")
        return np.array(t_list), np.array(rst)


def auto_get_h(method, elements, t_list, rst, default_h, error_bound):
    if (len(rst) < 4 and method == 'trap') or (len(rst) < 3 and method == 'be'):
        return default_h
    h = default_h
    for ele in elements.values():
        if isinstance(ele, cap):
            if method == 'trap':
                v_diff_1 = ele.get_tran_current(rst[-2]) - ele.get_tran_current(rst[-3])
                v_diff_2 = ele.get_tran_current(rst[-1]) - ele.get_tran_current(rst[-2])
                i_diff_1 = v_diff_1 / (t_list[-2] - t_list[-3] + minus)
                i_diff_2 = v_diff_2 / (t_list[-1] - t_list[-2] + minus)
                h_permitted = math.sqrt(abs(12 * ele.val / (i_diff_1 - i_diff_2 + minus) * error_bound))
                h = min(h, h_permitted)
            else:
                pass
        if isinstance(ele, ind):
            if method == 'trap':
                [v1, v2, v3] = [ele.pos_node.get_voltage(i) - ele.neg_node.get_voltage(i) for i in rst[-3:]]
                v_diff_1 = (v2 - v1) / (t_list[-2] - t_list[-3] + minus)
                v_diff_2 = (v3 - v2) / (t_list[-1] - t_list[-2] + minus)
                h_permitted = math.sqrt(abs(12 * ele.val / (v_diff_1 - v_diff_2 + minus) * error_bound))
                h = min(h, h_permitted)
            else:
                pass
    return h


def tran_solver(ground_node, basic_len, elements_dict, linear, error_bound, max_iter, t, h, rst_last, method='trap'):
    new_rst = basic_solver(ground_node, basic_len, elements_dict, 'tran', linear, t=t, h=h, last_time=rst_last,
                           last_itr=None, method=method)
    if not linear:
        old_rst = np.ones(shape=new_rst.shape) * np.Inf
        iter_num = 0

        while np.linalg.norm(new_rst - old_rst, np.Inf) > error_bound or iter_num > max_iter:
            old_rst = new_rst
            new_rst = basic_solver(ground_node, basic_len, elements_dict, 'tran', linear, t=t, h=h, last_time=rst_last,
                                   last_itr=old_rst, method=method)
            iter_num += 1
        if iter_num > max_iter:
            print("Warning: iteration reach maximum number and the circuit may not converge!")
    return new_rst
