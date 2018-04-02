import numpy as np


class task():
    pass


class dc_task(task):
    def __init__(self, src1, start1, stop1, incr1, src2=None, start2=None, stop2=None, incr2=None):
        self.src1, self.start1, self.stop1, self.incr1 = src1, start1, stop1, incr1
        if src2 is not None:
            self.src2, self.start2, self.stop2, self.incr2 = src2, start2, stop2, incr2

    def generate_seq(self):
        return list(np.arange(self.start1, self.stop1, self.incr1))


class ac_task(task):
    def __init__(self, number, start, stop, mode='dec'):
        self.mode = mode
        self.number = number
        self.start = start
        self.stop = stop

    # TODO:need to modify to sopport more mode
    def generate_seq(self):
        return [self.start + (self.stop - self.start) / self.number * i for i in range(self.number)]


class tran_task(task):
    def __init__(self, step, stop, start=0, max=-1):
        self.step, self.stop, self.start = step, stop, start
        h = min(self.step, (self.stop - self.start) / 50)
        self.h = min(h, max) if max != -1 else h

    def generate_seq(self):
        return list(np.arange(0, self.stop, self.h))

    def cut_seq(self, seq):
        return seq[int((self.start - 0) / self.h):]


class display_task(task):
    def __init__(self, mode, variable_list):
        self.mode = mode
        self.variable_list = variable_list


class plot_task(display_task):
    def __init__(self, mode, variable_list):
        display_task.__init__(self, mode, variable_list)


class print_task(display_task):
    def __init__(self, mode, variable_list):
        display_task.__init__(self, mode, variable_list)


