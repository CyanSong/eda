title

*netlist example 1
c1 1 0 5
r2 2 1 2
g5 1 0 2 1 4
v3 1 2 3
r4 2 0 8
.tran .2 200 10
.plot tran i(v3)
.dc v3 0 200 10
.print dc v(3) v(v3) v(3,0) i(v3)
.end