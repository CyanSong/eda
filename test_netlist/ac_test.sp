title

*netlist example 1
r2 2 1  2
v2 0 1 ac 10
c1 0 2 10


.ac dec 10 1 1000
.plot ac vm(2) vm(1)


.end