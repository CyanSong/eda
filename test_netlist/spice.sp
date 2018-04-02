title

*netlist example 1
c1 1 0 5
r2 2 1 2
g5 1 0 2 1 4
v3 1 2 3
r4 2 0 8
.tran .2 200 0 0.01
.plot tran v(2)
.end