import cmath

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import interactive

from command.ac_cmd import ac_handler
from command.dc_cmd import dc_handler
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
        elif self.part == 'db':
            return 20 * np.log10(rst)

    def toString(self):
        if self.element_name is not None:
            return "{}({})/{}".format(self.vi_type, self.element_name, "V" if self.vi_type == 'v' else "A").capitalize()
        else:
            return "{}({},{})/{}".format(self.vi_type, self.val_diff[0], self.val_diff[1],
                                         "V" if self.vi_type == 'v' else "A")


class display_handler(handler):
    def __init__(self, net, task, rst):
        handler.__init__(self, net, task)
        try:
            self.task_handler = rst[task.mode]
        except KeyError:
            raise net_definition_error(
                "{} simulation has not been defined, therefore can not be displayed!".format(task.mode))

    def handle(self):
        return [self.get_rst(i) for i in self.task.variable_list]

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
            return var.toString(), seq, var.format_rst(val_diff_rst)
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
            return var.toString(), seq, var.format_rst(tran_rst)


class plot_handler(display_handler):
    def __init__(self, net, t, rst):
        super().__init__(net, t, rst)

    def handle(self):
        print("Begin to plot...")
        rst = super().handle()
        mode = self.get_x_mode()
        if len(rst) > 1:
            plt.figure(figsize=(4 * len(rst), 4))
            for i, single_rst in enumerate(rst):
                plt.subplot(1, len(rst), i + 1)
                xlabel, ylable = self.get_labels(single_rst)
                if mode != 'lin':
                    plt.semilogx(single_rst[1], single_rst[2], marker='.')
                else:
                    plt.scatter(single_rst[1], single_rst[2], marker='.')
                plt.xlabel(xlabel)
                plt.ylabel(ylable)
        else:
            xlabel, ylable = self.get_labels(rst[0])
            if mode != 'lin':
                plt.semilogx(rst[0][1], rst[0][2], marker='.')
            else:
                plt.scatter(rst[0][1], rst[0][2], marker='.')
            plt.xlabel(xlabel)
            plt.ylabel(ylable)
        interactive(False)
        plt.show()
        print("Finish the plot.")

    def get_x_mode(self):
        if isinstance(self.task_handler, ac_handler):
            return self.task_handler.get_axis_mode()
        else:
            return 'lin'

    def get_labels(self, single_rst):
        if isinstance(self.task_handler, ac_handler):
            return "freq(Hz)", single_rst[0]
        elif isinstance(self.task_handler, dc_handler):
            return self.task_handler.task.src1, single_rst[0]
        else:
            return "t/s", single_rst[0]


class print_handler(display_handler):
    def __init__(self, net, t, rst):
        super().__init__(net, t, rst)

    def handle(self):
        rst = super().handle()
        for single_rst in rst:
            print(single_rst[1], single_rst[2])
