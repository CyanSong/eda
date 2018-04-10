title

*netlist example 1
r2 2 1  2
v2 0 1 ac 10
c1 0 2 1


.ac 10000 0.1 20
.plot ac vm(1) vm(2)


.end