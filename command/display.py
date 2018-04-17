import cmath

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import interactive

from command.handler import *
from error import net_definition_error


class variable():
    def __init__(self, vi_type, part, val_diff, element_name):
        self.vi_type, self.part, self.val_diff, self.element_name = vi_type, part, val_diff, element_name

    def format_rst(self, rst):
        if self.part == 'whole':
            return rst
        elif self.part == 'real':
            return rst.real
        elif self.part == 'img':
            return rst.imag
        elif self.part == 'mag':
            return np.abs(rst)
        elif self.part == 'phase':
            return np.vectorize(cmath.phase)(rst)
        else:
            pass


class display_handler(handler):
    def __init__(self, net, task, rst):
        handler.__init__(self, net, task)
        try:
            self.task_handler = rst[task.mode]
        except KeyError:
            raise net_definition_error(
                "{} simulation has not been defined, therefore can not be displayed!".format(task.mode))

    def handle(self):
        return np.array([self.get_rst(i) for i in self.task.variable_list])

    def get_rst(self, var):
        print("Fetching the result...")
        seq, rst = self.task_handler.handle()
        if var.vi_type == 'v':
            val_diff = var.val_diff
            if var.element_name is not None:
                try:
                    device = self.net.elements[var.element_name]
                except KeyError:
                    raise net_definition_error("this element {} is not defined".format(var.element_name))
                val_diff = (device.pos_node.num, device.neg_node.num)
            try:
                val_diff = (self.net.node_dict[val_diff[0]].num, self.net.node_dict[val_diff[1]].num)
            except KeyError:
                raise net_definition_error("this node {} or node {} is not defined".format(val_diff[0], val_diff[1]))
            val_diff_rst = np.array([val[val_diff[0]] - val[val_diff[1]] for val in rst])
            if self.task.mode == 'tran':
                seq_select = self.task_handler.task.cut_seq(seq)
                seq, val_diff_rst = seq[seq_select], val_diff_rst[seq_select]
            return seq, var.format_rst(val_diff_rst)
        else:
            try:
                ele = self.net.elements[var.element_name]
            except KeyError:
                raise net_definition_error("this element {} is not defined".format(var.element_name))
            if self.task.mode == 'ac':
                tran_rst = np.array([ele.get_current(single_rst, seq[i]) for i, single_rst in
                                     enumerate(rst)])
            elif self.task.mode == 'dc':
                tran_rst = np.array([ele.get_current(i) for i in rst])
            else:
                tran_rst = np.array([ele.get_current(i) for i in rst])
                seq_select = self.task_handler.task.cut_seq(seq)
                seq, val_diff_rst = seq[seq_select], tran_rst[seq_select]
            return seq, var.format_rst(tran_rst)


class plot_handler(display_handler):
    def __init__(self, net, t, rst):
        super().__init__(net, t, rst)

    def handle(self):
        print("Begin to plot...")
        rst = super().handle()
        if len(rst) > 1:
            plt.subplot()
            for i, single_rst in enumerate(rst):
                plt.scatter(single_rst[0], single_rst[1], marker='.')
        else:
            plt.scatter(rst[0][0], rst[0][1], marker='.')
        interactive(False)
        plt.show()
        print("Finish the plot.")


class print_handler(display_handler):
    def __init__(self, net, t, rst):
        super().__init__(net, t, rst)

    def handle(self):
        rst = super().handle()
        for single_rst in rst:
            print(single_rst[0], single_rst[1])
