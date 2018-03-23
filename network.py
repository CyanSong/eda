from spice_parser import spice_parser
from error import *
import numpy as np
from device.vcvs import vcvs
from device.ccvs import ccvs
from device.cccs import cccs
from device.vccs import vccs
from device.res import res
from device.vdc import vdc
from device.idc import idc


def parse_value(value_tree):
    # TODO9/*-+
    return float(value_tree.children[0].value)


def getNode(nodeNameList, nodeDict):
    res = []
    for nodeName in nodeNameList:
        if nodeName not in nodeDict:
            t = node(nodeName, len(nodeDict))
            nodeDict[nodeName] = t
        res.append(nodeDict[nodeName])
    return res


class node():
    def __init__(self, name, number):
        self.name = name
        self.num = number
        self.voltage = None

    def get_voltage(self):
        if self.voltage is None:
            print("get voltage before assignment!")
            exit()
        return self.voltage

    def put_voltage(self, val):
        self.voltage = val


class network():
    def __init__(self, code):
        self.parser = spice_parser
        try:
            self.tree = self.parser.parse(code)
        except:
            raise parser_syntax_error("bad syntax!")
        self.elements, self.nodeDict = self.build()
        # need to handle the command

    def build(self):
        elements = dict()
        node_dict = dict()
        definition = self.tree.children[1]
        for element in definition.children:
            if element.data == "element":
                ele = self.add_element(element.children[0], node_dict)
                if ele.name not in elements.keys():
                    elements[ele.name] = ele
                else:
                    raise net_definition_error("same name for different devices!")
        if "0" not in node_dict.keys():
            raise net_definition_error("You must assign the ground node as 0!")
        for element in elements.values():
            if isinstance(element, ccvs) or isinstance(element, cccs):
                element.v_src = elements["v" + element.v_src.children[0].value]
        return elements, node_dict

    def add_element(self, element, nodeDict):
        if element.data == 'res':
            nodes = getNode([i.value for i in element.children[1:3]], nodeDict)
            e = res("r" + element.children[0].value, nodes[0], nodes[1], parse_value(element.children[3]))
        elif element.data == 'vccs':
            nodes = getNode([i.value for i in element.children[1:5]], nodeDict)
            e = vccs("g" + element.children[0].value, nodes[0], nodes[1], nodes[2], nodes[3],
                     parse_value(element.children[5]))
        elif element.data == 'idc':
            nodes = getNode([i.value for i in element.children[1:3]], nodeDict)
            e = idc("i" + element.children[0].value, nodes[0], nodes[1], parse_value(element.children[3]))
        elif element.data == 'vdc':
            nodes = getNode([i.value for i in element.children[1:3]], nodeDict)
            e = vdc("v" + element.children[0].value, nodes[0], nodes[1], parse_value(element.children[3]))
        elif element.data == 'cccs':
            nodes = getNode([i.value for i in element.children[1:3]], nodeDict)
            e = cccs("f" + element.children[0].value, nodes[0], nodes[1], element.children[3],
                     parse_value(element.children[4]))
        elif element.data == 'vcvs':
            nodes = getNode([i.value for i in element.children[1:5]], nodeDict)
            e = vcvs("e" + element.children[0].value, nodes[0], nodes[1], nodes[2], nodes[3],
                     parse_value(element.children[5]))
        elif element.data == 'ccvs':
            nodes = getNode([i.value for i in element.children[1:3]], nodeDict)
            e = ccvs("h" + element.children[0].value, nodes[0], nodes[1], element.children[3],
                     parse_value(element.children[4]))
        else:
            nodes = []
            e = None
        return e

    def generate_linear_equation(self):
        index = 0
        v_node_num = len(self.nodeDict)
        for i in self.elements.values():
            if isinstance(i, vdc) or isinstance(i, vcvs) or isinstance(i, ccvs):
                i.put_index(index + v_node_num)
                index += 1
        return np.zeros((v_node_num + index, v_node_num + index)), np.zeros((v_node_num + index, 1))

    # This is a naive dc solver just for test
    def dc_handler(self, task):
        rst = self.dc_solver()
        self.put_dc_rst(rst)
        for n in self.nodeDict.values():
            print(n.name, n.get_voltage())
        for element in self.elements.values():
            print(element.name, element.get_dc_current())

    def dc_solver(self):
        a, b = self.generate_linear_equation()
        for i in self.elements.values():
            i.make_stamp(a, b)
        ground_node = self.nodeDict["0"].num
        index = list(range(len(a)))
        index.remove(ground_node)
        a, b = a[np.ix_(index, index)], b[np.ix_(index, [0])]
        rst = list(np.linalg.solve(a, b))
        rst.insert(ground_node, [0])
        return np.array(rst)

    def put_dc_rst(self, rst_mat):
        for i in self.nodeDict.values():
            i.put_voltage(rst_mat[i.num][0])
        for i in self.elements.values():
            if hasattr(i, "index"):
                i.put_dc_current(rst_mat[i.index][0])
