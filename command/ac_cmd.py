import numpy as np
from basic import *


def get_ac(cmd_tree):
    pass


# This is a naive dc solver just for test
def ac_handler(net, task):
    rst = ac_solver(net, 3000)
    # save rst

    # handle task
    for n in net.nodeDict.values():
        print(n.name, n.get_voltage(rst))
    for element in net.elements.values():
        print(element.name, element.get_current(rst, 3000))
    return rst

def ac_solver(net, freq):
    a, b = generate_linear_equation('ac')
    for i in net.elements.values():
        i.make_stamp(a, b, freq)
    ground_node = net.nodeDict["0"].num
    index = list(range(len(a)))
    index.remove(ground_node)
    a, b = a[np.ix_(index, index)], b[np.ix_(index, [0])]
    rst = list(np.linalg.solve(a, b))
    rst.insert(ground_node, [0])
    return np.array(rst)
