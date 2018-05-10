title

*netlist example 1

d1 2 0 model1
r1 1 2 1
v1 1 0 sin(0 2 1 0 1)
.tran .2 5 0 .05
.plot tran   v(2)
.end