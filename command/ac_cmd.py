import numpy as np
from basic import *
from multiprocessing.pool import ThreadPool
from time import time


def get_ac(cmd):
    task = dict()
    if len(cmd.children) == 4:
        task['mode'] = cmd.children[0]
        task['number'] = parse_value(cmd.children[1], int)
        task['start'] = parse_value(cmd.children[2], float)
        task['stop'] = parse_value(cmd.children[3], float)
    else:
        task['mode'] = 'dec'
        task['number'] = parse_value(cmd.children[0], int)
        task['start'] = parse_value(cmd.children[1], float)
        task['stop'] = parse_value(cmd.children[2], float)
    return task


# This is a naive dc solver just for test
def ac_handler(net, task):
    arg = [(net, task['start'] + (task['stop'] - task['start']) / task['number'] * i) for i in range(task['number'])]
    with ThreadPool(4) as pool:
        rst = pool.starmap(ac_solver, arg)
    return rst


def ac_solver(net, freq):
    a, b = generate_linear_equation(net, 'ac')
    for i in net.elements.values():
        i.make_stamp(a, b, freq)
    ground_node = net.node_dict["0"].num
    index = list(range(len(a)))
    index.remove(ground_node)
    a, b = a[np.ix_(index, index)], b[np.ix_(index, [0])]
    print("MNA",a,b)
    rst = list(np.linalg.solve(a, b))
    rst.insert(ground_node, [0])
    return np.array(rst)
