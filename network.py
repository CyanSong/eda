from spice_parser import *
from error import *
from basic import *
import numpy as np
from device.vcvs import vcvs, get_vcvs
from device.ccvs import ccvs, get_ccvs
from device.cccs import cccs, get_cccs
from device.vccs import vccs, get_vccs
from device.res import res, get_res
from device.vsrc import vsrc, get_vsrc
from device.isrc import isrc, get_isrc
from device.cap import cap, get_cap
from device.ind import ind, get_ind
from command.ac_cmd import *
from command.dc_cmd import *


class network():
    def __init__(self, code):
        code = pre_compile(code)
        self.parser = spice_parser
        try:
            self.tree = self.parser.parse(code)
        except Exception:
            raise parser_syntax_error("bad syntax!")
        self.elements, self.node_dict = self.build()
        self.handle_cmds()

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

    def add_element(self, element, node_dict):
        if element.data == 'res':
            return get_res(element, node_dict)
        elif element.data == 'vccs':
            return get_vccs(element, node_dict)
        elif element.data == 'isrc':
            return get_isrc(element, node_dict)
        elif element.data == 'vsrc':
            return get_vsrc(element, node_dict)
        elif element.data == 'cccs':
            return get_cccs(element, node_dict)
        elif element.data == 'vcvs':
            return get_vcvs(element, node_dict)
        elif element.data == 'ccvs':
            return get_ccvs(element, node_dict)
        elif element.data == 'cap':
            return get_cap(element, node_dict)
        elif element.data == "induc":
            return get_ind(element, node_dict)

    def handle_cmds(self):
        commands = self.tree.children[2]
        rst = []
        for command in commands.children:
            if command.data == "command":
                cmd_tree = command.children[0]
                if cmd_tree.data == 'acdef':
                    rst.append(ac_handler(self, get_ac(cmd_tree)))
                elif cmd_tree.data == 'dcdef':
                    rst.append(dc_handler(self, get_dc(cmd_tree)))
                else:
                    pass
