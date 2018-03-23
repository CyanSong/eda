from device.linear_device import linear_device
class Vdc(linear_device):
    def __init__(self,name,pos_node,neg_node,val):
        linear_device.__init__(self,name,pos_node,neg_node,val)
    def put_index(self,index):
        self.index=index
    def put_dc_current(self,current):
        self.current=current
    def get_dc_current(self):
        if self.current is not None:
            return self.current
        else:
            #need to modify
            print("get currrent before solve")
            exit()
    def make_stamp(self,mat,vec):
        mat[self.index][self.pos_node.num]+=1
        mat[self.index][self.neg_node.num]-=1
        mat[self.pos_node.num][self.index]+=1
        mat[self.neg_node.num][self.index]-=1
        vec[self.index]+=self.val