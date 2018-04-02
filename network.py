from command.ac_cmd import *
from command.dc_cmd import *
from command.tran_cmd import *
from command.display import *
from syntax.get_object import *
from device.cccs import cccs
from device.ccvs import ccvs
from error import *
from syntax.spice_parser import *


class network():
    def __init__(self, code):
        code = pre_compile(code)
        self.parser = spice_parser
        try:
            self.tree = self.parser.parse(code)
        except Exception as err:
            print(err)
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
                vname = "v" + element.v_src.children[0].value
                try:
                    element.v_src = elements[vname]
                except KeyError:
                    raise net_definition_error("this element {} is not defined".format(vname))
        return elements, node_dict

    def add_element(self, element, node_dict):
        element_type = element.data
        return get_device[element_type](element, node_dict)

    def handle_cmds(self):
        commands = self.tree.children[2]
        rst = dict()
        for command in commands.children:
            if command.data == "command":
                cmd_tree = command.children[0]
                if cmd_tree.data == 'acdef':
                    rst['ac'] = ac_handler(self, get_ac_task(cmd_tree))
                elif cmd_tree.data == 'dcdef':
                    rst['dc'] = dc_handler(self, get_dc_task(cmd_tree))
                elif cmd_tree.data == 'trandef':
                    rst['tran'] = tran_handler(self, get_tran_task(cmd_tree))
                elif cmd_tree.data == 'plot':
                    plot_handler(self, get_display_task(cmd_tree, 'plot'), rst).handle()
                elif cmd_tree.data == 'print':
                    print_handler(self, get_display_task(cmd_tree, 'print'), rst).handle()
                else:
                    pass
