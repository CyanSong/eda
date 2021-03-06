from ..basic import *
from ..command import display
from ..command import task
from ..device import diode
from ..device import mos
from ..device.cap import *
from ..device.cccs import *
from ..device.ccvs import *
from ..device.ind import *
from ..device.isrc import *
from ..device.res import *
from ..device.vccs import *
from ..device.vcvs import *
from ..device.vsrc import *


def get_res(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "r" + element_tree.children[0].value
    val = parse_value(element_tree.children[3])
    return res(name, nodes[0], nodes[1], val)


def get_cap(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "c" + element_tree.children[0].value
    val = parse_value(element_tree.children[3])
    return cap(name, nodes[0], nodes[1], val)


def get_cccs(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "f" + element_tree.children[0].value
    vsrc_name = element_tree.children[3]
    val = parse_value(element_tree.children[4])
    return cccs(name, nodes[0], nodes[1], vsrc_name, val)


def get_ccvs(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "h" + element_tree.children[0].value
    val = parse_value(element_tree.children[4])
    vsrc_name = element_tree.children[3]
    return ccvs(name, nodes[0], nodes[1], vsrc_name, val)


def get_ind(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "l" + element_tree.children[0].value
    val = parse_value(element_tree.children[3])
    return ind(name, nodes[0], nodes[1], val)


def get_isrc(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "i" + element_tree.children[0].value
    val = parse_value(element_tree.children[3])
    return isrc(name, nodes[0], nodes[1], val)


def get_vccs(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:5]], node_dict)
    name = "g" + element_tree.children[0].value
    val = parse_value(element_tree.children[5])
    return vccs(name, nodes[0], nodes[1], nodes[2], nodes[3], val)


def get_vcvs(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:5]], node_dict)
    name = "e" + element_tree.children[0].value
    val = parse_value(element_tree.children[5])
    return vcvs(name, nodes[0], nodes[1], nodes[2], nodes[3], val)


def get_vsrc(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "v" + element_tree.children[0].value
    spec = element_tree.children[3]
    if spec.data == 'vdc':
        src_type = 'dc'
        dc_val = parse_value(spec.children[-1], float)
        return vsrc(name, nodes[0], nodes[1], src_type=src_type, dc_val=dc_val)
    elif spec.data == 'vac':
        src_type = 'ac'
        ac_mag = parse_value(spec.children[0]) if len(spec.children) > 0 else 0
        ac_phase = parse_value(spec.children[1]) if len(spec.children) > 1 else 0
        return vsrc(name, nodes[0], nodes[1], src_type, ac_mag=ac_mag, ac_phase=ac_phase)
    else:
        src_type = 'fun'
        return vsrc(name, nodes[0], nodes[1], src_type, fun=get_fun(spec))


def get_diode(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "d" + element_tree.children[0].value
    model_name = element_tree.children[3].data
    if True:  # modify according to model name
        if len(element_tree.children) == 5:
            ic = parse_value(element_tree.children[4], float)
            return diode.diode(name, nodes[0], nodes[1], ic=ic)
        else:
            return diode.diode(name, nodes[0], nodes[1])


def get_mos(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:5]], node_dict)
    name = "m" + element_tree.children[0].value
    model_name = element_tree.children[5].data
    if len(element_tree.children) == 8:
        w = parse_value(element_tree.children[6], float)
        l = parse_value(element_tree.children[7], float)
        return mos.mos(name, nodes[0], nodes[1], nodes[2], nodes[3], model_name, w, l)
    else:
        return mos.mos(name, nodes[0], nodes[1], nodes[2], nodes[3], model_name)


get_device = {'vsrc': get_vsrc, 'cap': get_cap, 'induc': get_ind, 'isrc': get_isrc, 'vccs': get_vccs, 'vcvs': get_vcvs,
              'ccvs': get_ccvs, 'cccs': get_cccs, 'res': get_res, 'diode': get_diode, 'mos': get_mos}


def get_variable(variable_tree):
    point_of_val = variable_tree.children[-1]
    if point_of_val.data == 'valofpoint':
        element_name = None
        val_diff = (point_of_val.children[0].value, '0')
    elif point_of_val.data == 'diffofpoint':
        element_name = None
        val_diff = (point_of_val.children[0].value, point_of_val.children[1].value)
    else:
        val_diff = None
        element_name = point_of_val.children[0].data + point_of_val.children[1].value
    if len(variable_tree.children) == 3:
        part = variable_tree.children[1].data
        return display.variable(variable_tree.children[0].data, part, val_diff, element_name)
    else:
        return display.variable(variable_tree.children[0].data, 'whole', val_diff, element_name)


def get_fun(fun_tree):
    if fun_tree.data == 'pulse':
        return pulse(*[parse_value(i, float) for i in fun_tree.children])
    elif fun_tree.data == 'sin':
        return sin(*[parse_value(i, float) for i in fun_tree.children])


def get_display_task(cmd_tree, display_mode):
    mode = cmd_tree.children[0].data
    var_list = [get_variable(i) for i in cmd_tree.children[1:]]
    return task.print_task(mode, var_list) if display_mode == 'print' else task.plot_task(mode, var_list)


def get_ac_task(cmd):
    return task.ac_task(parse_value(cmd.children[1], int), parse_value(cmd.children[2], float),
                       parse_value(cmd.children[3], float), cmd.children[0].data)


def get_dc_task(cmd_tree):
    if len(cmd_tree.children) == 1:
        src = cmd_tree.children[0].children[0]
        vsrc = src.children[0].data + src.children[1].value
        dsrc = [parse_value(i, float) for i in cmd_tree.children[0].children[1:]]
        return task.dc_task(vsrc, dsrc[0], dsrc[1], dsrc[2])
    else:
        pass


def get_tran_task(cmd_tree):
    seq = [parse_value(i, float) for i in cmd_tree.children]
    return task.tran_task(*seq)
