from command.ac_cmd import *
from command.dc_cmd import *
from command.tran_cmd import *
from device.cccs import *
from device.ccvs import *
from device.ind import *
from error import *
from syntax.get_object import *
from syntax.spice_parser import *


class network():
    def __init__(self, code):
        self.code = pre_compile(code)
        self.parser = spice_parser
        self.linear = True
        self.parse()
        self.elements, self.node_dict = self.build()
        self.handle_cmds()

    def parse(self):
        print("Begin to parse the netlist...")
        try:
            self.tree = self.parser.parse(self.code)
            #print(self.tree)
        except Exception as err:
            raise parser_syntax_error("Bad syntax!\n" + str(err))
        print("Finish the parsing of netlist.")

    def build(self):
        print("Begin to build the circuit...")
        elements = dict()
        node_dict = dict()
        definition = self.tree.children[1]
        for element in definition.children:
            if element.data == "element":
                ele = self.add_element(element.children[0], node_dict)
                if not isinstance(ele, linear_device):
                    self.linear = False
                if ele.name not in elements.keys():
                    elements[ele.name] = ele
                else:
                    raise net_definition_error("Same name for different devices!")
        if "0" not in node_dict.keys():
            raise net_definition_error("You must assign the ground node as 0!")
        for element in elements.values():
            if isinstance(element, ccvs) or isinstance(element, cccs):
                vname = "v" + element.v_src.children[0].value
                try:
                    element.v_src = elements[vname]
                except KeyError:
                    raise net_definition_error("The element: {} is not defined".format(vname))
        print("Finish to build the circuit.")
        return elements, node_dict

    def add_element(self, element, node_dict):
        element_type = element.data
        ele = get_device[element_type](element, node_dict)
        print("----Add element {}".format(ele.name))
        return ele

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


"""
    def draw(self):
        d = schem.Drawing()

        def mapping(ele):
            if isinstance(ele, res):
                return e.RES
            elif isinstance(ele, cap):
                return e.CAP
            elif isinstance(ele, vsrc):
                return e.SOURCE_V
            else:
                pass

        nodeD = dict()
        ori = 'down'
        for element in self.elements.values():
            x = nodeD[element.pos_node.num] if element.pos_node.num in nodeD.keys() else None
            y = nodeD[element.neg_node.num] if element.neg_node.num in nodeD.keys() else None

            print(ori)
            if x is None and y is None:
                tmp = d.add(mapping(element), label=str(element.val))
            elif x is None and y is not None:
                tmp = d.add(mapping(element), label=str(element.val),to=y,d=ori)
                ori = 'right' if ori == 'down' else 'down'
            elif x is not None and y is not None:
                tmp = d.add(mapping(element), label=str(element.val),xy=x,to=y)
            else:
                tmp = d.add(mapping(element), label=str(element.val),xy=x,d=ori)
                ori = 'right' if ori == 'down' else 'down'

            nodeD[element.pos_node.num] = tmp.start
            nodeD[element.neg_node.num] = tmp.end

        d.draw()
"""
