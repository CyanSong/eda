from device.device import device


class linear_device(device):
    def __init__(self, name, pos_node, neg_node, val):
        device.__init__(self, name)
        self.pos_node = pos_node
        self.neg_node = neg_node
        self.val = val

    def get_voltage_diff(self):
        return self.pos_node.get_voltage() - self.neg_node.get_voltage()
