#! /home/cyan/eda_env/eda/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from device.vcvs import VCVS
from device.ccvs import CCVS
from device.cccs import CCCS
from device.vccs import VCCS
from device.res import res
from device.vdc import Vdc
from device.idc import idc
from parser import spice_parser


def parse_value(valueTree):
    #TODO9/*-+
    return float(valueTree.children[0].value)

def getNode(nodeNameList,nodeDict):
    res=[]
    for nodeName in nodeNameList:
        if nodeName not in nodeDict:
            t=node(nodeName,len(nodeDict))
            nodeDict[nodeName]=t
        res.append(nodeDict[nodeName])
    return res


class node():
    def __init__(self,name,number):
        self.name=name
        self.num=number
        self.voltage=None
    def get_voltage(self):
        if self.voltage is None:
            print("get voltage before assignment!")
            exit()
        return self.voltage
    def put_voltage(self,val):
        self.voltage=val


class network():
    def __init__(self,code):
        self.parser=spice_parser
        try:
            self.tree=self.parser.parse(code)
        except:
            #need to modify
            print("bad syntax!")
            exit()
        self.elements,self.nodeDict=self.build()
        #need to handle the command

    def build(self):
        elements=dict()
        nodeDict=dict()
        definition=self.tree.children[1]
        for element in definition.children:
            if element.data=="element":
                ele=self.add_element(element.children[0],nodeDict)
                if ele.name not in elements.keys():
                    elements[ele.name]=ele
                else:
                    #need to modify
                    print("same name for different devices!")
                    exit()
        if "0" not in nodeDict.keys():
            #need to modify
            print("You must assign the ground node as 0!")
            exit()
        for element in elements.values():
            if isinstance(element,CCVS) or isinstance(element,CCCS):
                element.vsrc=elements["v"+element.vsrc.children[0].value]
        return elements,nodeDict

    def add_element(self,element,nodeDict):
        if element.data=='res':
            nodes=getNode([i.value for i in element.children[1:3]],nodeDict)
            e=res("r"+element.children[0].value,nodes[0],nodes[1],parse_value(element.children[3]))
        elif element.data=='vccs':
            nodes=getNode([i.value for i in element.children[1:5]],nodeDict)
            e=VCCS("g"+element.children[0].value,nodes[0],nodes[1],nodes[2],nodes[3],parse_value(element.children[5]))
        elif element.data=='idc':
            nodes=getNode([i.value for i in element.children[1:3]],nodeDict)
            e=idc("i"+element.children[0].value,nodes[0],nodes[1],parse_value(element.children[3]))
        elif element.data =='vdc':
            nodes=getNode([i.value for i in element.children[1:3]],nodeDict)
            e=Vdc("v"+element.children[0].value,nodes[0],nodes[1],parse_value(element.children[3]))
        elif element.data =='cccs':
            nodes=getNode([i.value for i in element.children[1:3]],nodeDict)
            e=CCCS("f"+element.children[0].value,nodes[0],nodes[1],element.children[3],parse_value(element.children[4]))
        elif element.data =='vcvs':
            nodes=getNode([i.value for i in element.children[1:5]],nodeDict)
            e=VCVS("e"+element.children[0].value,nodes[0],nodes[1],nodes[2],nodes[3],parse_value(element.children[5]))
        elif element.data =='ccvs':
            nodes=getNode([i.value for i in element.children[1:3]],nodeDict)
            e=CCVS("h"+element.children[0].value,nodes[0],nodes[1],element.children[3],parse_value(element.children[4]))
        else:
            nodes=[]
            e=None
        return e

    def generate_linear_equation(self):
        index=0
        vNodeNum=len(self.nodeDict)
        for i in self.elements.values():
            if isinstance(i,Vdc) or isinstance(i,VCVS) or isinstance(i,CCVS):        
                i.put_index(index+vNodeNum)
                index+=1
        return np.zeros((vNodeNum+index,vNodeNum+index)),np.zeros((vNodeNum+index,1))

    # This is a naive dc solver just for test
    def dc_handler(self,task):
        rst=self.dc_solver()
        self.put_dc_rst(rst)
        for node in self.nodeDict.values():
            print(node.name,node.get_voltage())
        for element in self.elements.values():
            print(element.name,element.get_dc_current())

    
    def dc_solver(self):
        a,b=self.generate_linear_equation()
        for i in self.elements.values():
            i.make_stamp(a,b)
        groundNode=self.nodeDict["0"].num
        index=list(range(len(a)))
        index.remove(groundNode)
        a,b=a[np.ix_(index,index)],b[np.ix_(index,[0])]
        rst=list(np.linalg.solve(a,b))
        rst.insert(groundNode,[0])
        return np.array(rst)
    
    def put_dc_rst(self,rst_mat):
        for i in self.nodeDict.values():
            i.put_voltage(rst_mat[i.num][0])
        for i in self.elements.values():
            if hasattr(i,"index"):
                i.put_dc_current(rst_mat[i.index][0])



