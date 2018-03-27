from device.vccs import vccs
from basic import *


def get_res(element_tree, node_dict):
    nodes = remap_node([i.value for i in element_tree.children[1:3]], node_dict)
    name = "r" + element_tree.children[0].value
    val = parse_value(element_tree.children[3])
    return res(name, nodes[0], nodes[1], val)



class res(vccs):
    def __init__(self, name, pos_node, neg_node, val):
        vccs.__init__(self, name, pos_node, neg_node, pos_node, neg_node, 1 / val)
