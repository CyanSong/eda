title

*netlist example 1
c1 1 0 5
r2 2 1 2
g5 1 0 2 1 4
v3 1 2 3
r4 2 0 8
.tran .2 1000 0 0.01
.print tran v(2) i(v3)
.end