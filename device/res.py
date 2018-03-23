from device.vccs import vccs


class res(vccs):
    def __init__(self, name, pos_node, neg_node, val):
        vccs.__init__(self, name, pos_node, neg_node, pos_node, neg_node, 1 / val)
