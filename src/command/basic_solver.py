from device.cap import *
from device.ind import *
from device.vsrc import *
from src.basic import *
from src.error import *


def basic_solver(ground_node, basic_len, elements_dict, type, linear, **kwargs):
    a, b = generate_linear_equation(basic_len, elements_dict, type)
    try:
        if not linear:
            last_itr = kwargs['last_itr']
        if type == "tran":
            last_time = kwargs['last_time']
            method = kwargs['method']
            h = kwargs['h']
            t = kwargs['t']
        elif type == 'ac':
            freq = kwargs['freq']
        else:
            vname = kwargs['vname']
            val = kwargs['val']
    except KeyError as e:
        raise internal_error("Lose argument {}".format(str(e)))

    for i in elements_dict.keys():
        if not isinstance(elements_dict[i], linear_device):
            elements_dict[i].make_stamp(type, a, b, last_itr=last_itr)
        else:
            if type == 'tran':
                if isinstance(elements_dict[i], cap) or isinstance(elements_dict[i], ind):
                    elements_dict[i].make_stamp(type, a, b, h=h, rst_last=last_time, method=method)
                elif isinstance(elements_dict[i], vsrc):
                    elements_dict[i].make_stamp(type, a, b, t=t)
                else:
                    elements_dict[i].make_stamp(type, a, b)
            elif type == 'dc':
                if i == vname:
                    elements_dict[i].make_stamp(type, a, b, val=val)
                else:
                    elements_dict[i].make_stamp(type, a, b)
            else:
                elements_dict[i].make_stamp(type, a, b, freq=freq)
    index = list(range(len(a)))
    index.remove(ground_node)
    a, b = a[np.ix_(index, index)], b[np.ix_(index, [0])]

    try:
        new_rst = list(np.linalg.solve(a, b))
    except np.linalg.linalg.LinAlgError:
        raise circuit_error("This circuit is not solvable!")

    new_rst.insert(ground_node, [0])
    new_rst = np.array(new_rst)[:, 0]

    return new_rst
