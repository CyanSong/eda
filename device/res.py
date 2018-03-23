from device.vccs import VCCS
class res(VCCS):
    def __init__(self,name,pos_node,neg_node,val):
        VCCS.__init__(self,name,pos_node,neg_node,pos_node,neg_node,1/val)
