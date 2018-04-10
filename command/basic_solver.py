from basic import *
from device.device import *
from error import *


def basic_solver(ground_node, basic_len, elements_dict, type, linear, **kwargs):
    a, b = generate_linear_equation(basic_len, elements_dict, type)
    freq = 0
    try:
        if not linear:
            last_itr = kwargs['last_itr']
        if type == "tran":
            last_time = kwargs['last_time']
            h = kwargs['h']
        elif type == 'ac':
            freq = kwargs['freq']
        else:
            vname = kwargs['vname']
            val = kwargs['val']
    except KeyError as e:
        raise internal_error("Lose argument {}".format(str(e)))

    for i in elements_dict.keys():
        if not isinstance(elements_dict[i], linear_device):
            elements_dict[i].make_stamp(a, b, freq, last_itr)
        else:
            if type == 'tran' and hasattr(elements_dict[i], 'make_tran_stamp'):
                elements_dict[i].make_tran_stamp(a, b, h, last_time)
            elif type == 'dc' and i == vname:
                elements_dict[i].make_stamp(a, b, 0, val)
            else:
                elements_dict[i].make_stamp(a, b, freq)

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
