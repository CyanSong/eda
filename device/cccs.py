from device.linear_device import linear_device
class CCCS(linear_device):
    def __init__(self,name,pos_node,neg_node,vsrc,val):
        linear_device.__init__(self,name,pos_node,neg_node,val)
        self.vsrc=vsrc
    def make_stamp(self,mat,vec):
        index=self.vsrc.index
        mat[self.pos_node.num][index]+=self.val
        mat[self.neg_node.num][index]-=self.val
    def get_dc_current(self):
        ctl_cur=self.vsrc.get_dc_current()
        return self.val*ctl_cur