class device():
    def __init__(self, name):
        self.name = name


class double_port_device(device):
    def __init__(self, name, pos_node, neg_node, val):
        device.__init__(self, name)
        self.pos_node = pos_node
        self.neg_node = neg_node
        self.val = val

    def get_voltage_diff(self, rst_vec):
        return self.pos_node.get_voltage(rst_vec) - self.neg_node.get_voltage(rst_vec)


class linear_device(double_port_device):
    def __init__(self, name, pos_node, neg_node, val):
        super().__init__(name, pos_node, neg_node, val)
