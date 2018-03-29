import numpy as np
from basic import *

def get_dc(cmd_tree):
    pass

# This is a naive dc solver just for test
def dc_handler(net, task):
    rst = dc_solver(net)

    for n in net.nodeDict.values():
        print(n.name, n.get_voltage(rst))
    for element in net.elements.values():
        print(element.name, element.get_current(rst))
    return rst

# This part also need to modify
def dc_solver(net):
    a, b = net.generate_linear_equation('dc')
    for i in net.elements.values():
        i.make_stamp(a, b, 0)
    ground_node = net.nodeDict["0"].num
    index = list(range(len(a)))
    index.remove(ground_node)
    a, b = a[np.ix_(index, index)], b[np.ix_(index, [0])]
    rst = list(np.linalg.solve(a, b))
    rst.insert(ground_node, [0])
    return np.array(rst)

