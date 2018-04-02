class handler():
    def __init__(self, net, t):
        self.task = t
        self.net = net

    def handle(self):
        ground_node = self.net.node_dict["0"].num
        basic_len = len(self.net.node_dict)
        elements = self.net.elements
        seq = self.task.generate_seq()
        return ground_node, basic_len, elements, seq
