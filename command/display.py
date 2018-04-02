import matplotlib.pyplot as plt
from command.handler import *
from error import net_definition_error


class variable():
    def __init__(self, vi_type, part, val_diff, element_name):
        self.vi_type, self.part, self.val_diff, self.element_name = vi_type, part, val_diff, element_name

    def format_rst(self, rst):
        if self.part == 'whole':
            return rst
        else:
            # TODO: support more format
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
        return [self.get_rst(i) for i in self.task.variable_list]

    def get_rst(self, var):
        rst = self.task_handler.handle()
        seq = self.task_handler.task.generate_seq()
        if var.vi_type == 'v':
            val_diff = var.val_diff
            if var.element_name is not None:
                try:
                    device = self.net.elements[var.element_name]
                except KeyError:
                    raise net_definition_error("this element {} is not defined".format(var.element_name))
                val_diff = (device.pos_node.name, device.neg_node.name)
            try:
                val_diff = (self.net.node_dict[val_diff[0]], self.net.node_dict[val_diff[1]])
            except KeyError:
                raise net_definition_error("this node {} or node {} is not defined".format(val_diff[0], val_diff[1]))
            val_diff_rst = [val[val_diff[0]] - val[val_diff[1]] for val in rst]
            return seq, val_diff_rst
        else:
            try:
                device = self.net.elements[var.element_name]
            except KeyError:
                raise net_definition_error("this element {} is not defined".format(var.element_name))
            if self.task.mode == 'ac':
                tran_rst = [device.get_current(single_rst, seq[i]) for i, single_rst in
                            enumerate(rst)]
            elif self.task.mode == 'dc':
                tran_rst = [device.get_current(single_rst) for single_rst in rst]
            else:
                tran_rst = [device.get_current(single_rst) for single_rst in rst]
                seq, tran_rst = self.task_handler.task.cut_seq(seq), self.task_handler.task.cut_seq(tran_rst)
            return seq, var.format_rst(tran_rst)


class plot_handler(display_handler):
    def __init__(self, net, t, rst):
        super().__init__(net, t, rst)

    # TODO modify to support GUI
    def handle(self):
        rst = super().handle()
        for single_rst in rst:
            plt.plot(single_rst[0], single_rst[1])
            plt.show()


class print_handler(display_handler):
    def __init__(self, net, t, rst):
        super().__init__(net, t, rst)

    # TODO modify to support GUI
    def handle(self):
        rst = super().handle()
        for single_rst in rst:
            print(single_rst[0])
            print(single_rst[1])
